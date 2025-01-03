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
    fields = [
        'name',
        'status',
        'progress',
        ('design_start_date', 'design_end_date'),
        ('shop_drawing_start_date', 'shop_drawing_end_date'),
        ('planned_start_date', 'planned_end_date'),
        'qc_status'
    ]
    classes = ('collapse',)
    verbose_name = "Building"
    verbose_name_plural = "Buildings"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_number', 'name', 'status', 'client_name', 'contract_date')
    list_filter = ('status', 'contract_date')
    search_fields = ('project_number', 'name', 'client_name')
    date_hierarchy = 'contract_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'estimation_number', 'project_number', 'name',
                'project_manager', 'client_name', 'status'
            ),
            'classes': ('wide',)
        }),
        ('Contract Dates', {
            'fields': (
                'contract_date', 'down_payment_date'
            ),
            'classes': ('collapse',)
        }),
        ('Project Details', {
            'fields': (
                'structure_type', 'number_of_structures',
                'erection_subcontractor', 'project_nature',
                'scope_of_work'
            ),
            'classes': ('collapse',)
        }),
        ('Contract Details', {
            'fields': (
                'incoterm', 'contractual_tonnage',
                'engineering_tonnage', 'area', 'm2_per_ton'
            ),
            'classes': ('collapse',)
        }),
        ('Payments', {
            'fields': (
                ('down_payment', 'down_payment_ack'),
                ('payment_2', 'payment_2_ack'),
                ('payment_3', 'payment_3_ack'),
                ('payment_4', 'payment_4_ack'),
                ('payment_5', 'payment_5_ack'),
                'preliminary_retention', 'ho_retention'
            ),
            'classes': ('collapse',)
        }),
        ('Technical Specifications', {
            'fields': (
                'galvanized', 'galvanization_microns',
                'welding_process', 'welding_wire_aws_class',
                'pqr_no', 'wps_no', 'standard_code'
            ),
            'classes': ('collapse',)
        }),
        ('Paint System', {
            'fields': (
                ('paint_coat_1', 'coat_1_microns', 'coat_1_liters_needed'),
                ('paint_coat_2', 'coat_2_microns', 'coat_2_liters_needed'),
                ('paint_coat_3', 'coat_3_microns', 'coat_3_liters_needed'),
                ('paint_coat_4', 'coat_4_microns', 'coat_4_liters_needed'),
                'top_coat_ral_number'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [BuildingInline]
    
    class Media:
        css = {
            'all': ('admin/css/forms.css',)
        }
        js = ('admin/js/collapse.js',)

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'project_number', 'status', 'progress',
        'design_start_date', 'shop_drawing_start_date',
        'planned_start_date', 'qc_status'
    ]
    list_filter = ['project', 'status', 'qc_status']
    search_fields = ['name', 'project__name', 'project__project_number']
    date_hierarchy = 'planned_start_date'
    
    def project_number(self, obj):
        return obj.project.project_number
    project_number.short_description = 'Project #'
    project_number.admin_order_field = 'project__project_number'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project', 'name', 'description'),
            'classes': ('wide',)
        }),
        ('Status', {
            'fields': ('status', 'progress'),
            'classes': ('wide',)
        }),
        ('Design Phase', {
            'fields': (('design_start_date', 'design_end_date'),),
            'classes': ('collapse',)
        }),
        ('Shop Drawing Phase', {
            'fields': (('shop_drawing_start_date', 'shop_drawing_end_date'),),
            'classes': ('collapse',)
        }),
        ('Production Phase', {
            'fields': (
                ('planned_start_date', 'planned_end_date'),
                ('actual_start_date', 'actual_end_date')
            ),
            'classes': ('collapse',)
        }),
        ('Quality Control', {
            'fields': (
                'qc_inspection_date',
                'qc_status',
                'qc_remarks'
            ),
            'classes': ('collapse',)
        })
    )

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
    list_display = [
        'id', 'project', 'building', 'log_designation', 'part_designation',
        'assembly_mark', 'part_mark', 'name_designation', 'quantity',
        'profile', 'grade', 'length', 'net_area_single', 'net_area_total',
        'single_part_weight', 'net_weight_total', 'revision'
    ]
    list_filter = ['project', 'building', 'part_designation', 'grade', 'revision']
    search_fields = [
        'id', 'log_designation', 'assembly_mark', 'part_mark', 
        'name_designation', 'profile', 'grade'
    ]
    ordering = ['id']

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
