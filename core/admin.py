from django.contrib import admin
from .models import (Material, ProductionProcess, Project, ProductionLog, QualityCheck, 
                    MaterialUsage, RawData, Facility, ProductionTeam, Personnel, Building, User)
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect
from django.urls import path
from django.contrib.auth import login
from django.contrib import messages

User = get_user_model()

# Register your models here.

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'unit', 'quantity', 'minimum_stock')
    search_fields = ('code', 'name')
    list_filter = ('unit',)

@admin.register(ProductionProcess)
class ProductionProcessAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    ordering = ('category', 'name')

class BuildingInline(admin.TabularInline):
    model = Building
    extra = 1
    fields = ['name', 'description']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_number', 'name', 'status', 'client_name')
    search_fields = ('project_number', 'name', 'client_name')
    list_filter = ('status',)
    fieldsets = (
        ('Project Information', {
            'fields': (
                'project_number', 'name',
                'client_name', 'status'
            )
        }),
    )
    inlines = [BuildingInline]

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'description']
    list_filter = ['project']
    search_fields = ['name', 'project__name']

@admin.register(ProductionLog)
class ProductionLogAdmin(admin.ModelAdmin):
    list_display = ('log_designation', 'process', 'production_date', 
                   'produced_quantity', 'facility', 'team', 'created_by')
    list_filter = ('production_date', 'facility', 'team', 'process')
    search_fields = ('log_designation', 'facility__name', 'team__name')
    date_hierarchy = 'production_date'
    autocomplete_fields = ['facility', 'team', 'created_by']

@admin.register(QualityCheck)
class QualityCheckAdmin(admin.ModelAdmin):
    list_display = ('production_log', 'inspector', 'parameter', 'measurement', 'result')
    search_fields = ('production_log__project__code', 'parameter')
    list_filter = ('result', 'inspector')

@admin.register(MaterialUsage)
class MaterialUsageAdmin(admin.ModelAdmin):
    list_display = ('production_log', 'material', 'quantity_used')
    search_fields = ('production_log__project__code', 'material__name')
    list_filter = ('material',)

@admin.register(RawData)
class RawDataAdmin(admin.ModelAdmin):
    list_display = ['row_id', 'project', 'assembly_mark', 'part_mark', 'quantity', 'profile', 'grade']
    list_filter = ['project', 'assembly_mark', 'grade']
    search_fields = ['row_id', 'project__project_number', 'assembly_mark', 'part_mark', 'profile', 'grade']
    readonly_fields = ['row_id', 'created_at', 'updated_at']

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description')
    ordering = ('name',)

@admin.register(ProductionTeam)
class ProductionTeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility', 'team_leader', 'is_active')
    list_filter = ('facility', 'is_active')
    search_fields = ('name', 'facility__name', 'team_leader__first_name', 'team_leader__last_name')
    autocomplete_fields = ['facility', 'team_leader']

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'first_name', 'last_name', 'role', 'facility', 'team', 'is_active')
    list_filter = ('role', 'facility', 'team', 'is_active')
    search_fields = ('employee_id', 'first_name', 'last_name')
    autocomplete_fields = ['facility', 'team']
    list_select_related = ('facility', 'team')

class CustomUserAdmin(UserAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<id>/switch/',
                self.admin_site.admin_view(self.switch_to_user),
                name='auth_user_switch',
            ),
        ]
        return custom_urls + urls

    def switch_to_user(self, request, id):
        if not request.user.is_superuser:
            messages.error(request, "You don't have permission to switch users.")
            return redirect('admin:auth_user_changelist')
        
        try:
            user = self.get_queryset(request).get(pk=id)
            login(request, user)
            messages.success(request, f'Successfully switched to {user.username}')
            return redirect('dashboard')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('admin:auth_user_changelist')

    def switch_user_button(self, obj):
        if obj.is_superuser:
            return ''
        return f'<a class="button" href="{ obj.pk }/switch/">Switch to User</a>'
    switch_user_button.short_description = 'Switch'
    switch_user_button.allow_tags = True

    list_display = UserAdmin.list_display + ('switch_user_button',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
