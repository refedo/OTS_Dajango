from django.contrib import admin
from .models import (
    BeamMaterial, SheetMaterial, AngleMaterial, PipeMaterial,
    TubeMaterial, PurlinMaterial, BarMaterial, FastenerMaterial,
    PanelMaterial, MiscMaterial, MaterialProperty
)

@admin.register(BeamMaterial)
class BeamMaterialAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'beam_type', 'height', 'width', 'weight_per_meter', 'quantity']
    list_filter = ['beam_type', 'grade']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(SheetMaterial)
class SheetMaterialAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'sheet_type', 'thickness', 'width', 'length', 'quantity']
    list_filter = ['sheet_type', 'grade']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(AngleMaterial)
class AngleMaterialAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'angle_type', 'height', 'width', 'thickness', 'quantity']
    list_filter = ['angle_type', 'grade']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(PipeMaterial)
class PipeMaterialAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'pipe_type', 'diameter', 'thickness', 'length', 'quantity']
    list_filter = ['pipe_type', 'grade', 'schedule']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(TubeMaterial)
class TubeMaterialAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'tube_type', 'height', 'width', 'thickness', 'quantity']
    list_filter = ['tube_type', 'grade']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(PurlinMaterial)
class PurlinMaterialAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'purlin_type', 'height', 'width', 'thickness', 'quantity']
    list_filter = ['purlin_type', 'grade']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(BarMaterial)
class BarMaterialAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'bar_type', 'get_dimensions', 'length', 'quantity']
    list_filter = ['bar_type', 'grade']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']

    def get_dimensions(self, obj):
        if obj.bar_type == 'ROUND':
            return f"Ø{obj.diameter}"
        elif obj.bar_type == 'SQUARE':
            return f"{obj.height}x{obj.height}"
        else:  # FLAT
            return f"{obj.height}x{obj.width}"
    get_dimensions.short_description = 'Dimensions'

@admin.register(FastenerMaterial)
class FastenerMaterialAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'fastener_type', 'diameter', 'length', 'thread_size', 'quantity']
    list_filter = ['fastener_type', 'grade', 'finish']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(PanelMaterial)
class PanelMaterialAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'panel_type', 'thickness', 'width', 'length', 'quantity']
    list_filter = ['panel_type']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(MiscMaterial)
class MiscMaterialAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'misc_type', 'quantity']
    list_filter = ['misc_type']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(MaterialProperty)
class MaterialPropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'unit', 'content_type', 'object_id']
    list_filter = ['content_type', 'name']
    search_fields = ['name', 'value']
