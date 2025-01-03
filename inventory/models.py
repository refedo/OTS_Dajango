from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator

class BaseMaterial(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=50)
    grade = models.CharField(max_length=50, null=True, blank=True)
    standard = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True)
    quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        default=0
    )
    minimum_stock = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.code} - {self.name}"

class BeamMaterial(BaseMaterial):
    BEAM_TYPES = [
        ('IPE-AA', 'IPE-AA Beam'),
        ('HEA', 'HEA Beam'),
        ('HEB', 'HEB Beam'),
        ('IPE', 'IPE Beam'),
        ('JIS', 'JIS Beam'),
        ('UB', 'UB Beam'),
        ('UPE', 'UPE Beam'),
        ('UPN', 'UPN Beam'),
        ('W', 'W Section'),
    ]
    
    beam_type = models.CharField(max_length=10, choices=BEAM_TYPES)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    flange_thickness = models.DecimalField(max_digits=10, decimal_places=2)
    web_thickness = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    weight_per_meter = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Beam'
        verbose_name_plural = 'Beams'

class SheetMaterial(BaseMaterial):
    SHEET_TYPES = [
        ('AL', 'Aluminum Sheet'),
        ('BLK', 'Black Sheet'),
        ('CHK', 'Checkered Plate'),
        ('GI', 'GI Sheet'),
        ('SS', 'Stainless Steel Sheet'),
    ]
    
    sheet_type = models.CharField(max_length=10, choices=SHEET_TYPES)
    thickness = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    surface_treatment = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Sheet'
        verbose_name_plural = 'Sheets'

class AngleMaterial(BaseMaterial):
    ANGLE_TYPES = [
        ('EQ', 'Equal Angle'),
        ('UEQ', 'UnEqual Angle'),
    ]
    
    angle_type = models.CharField(max_length=5, choices=ANGLE_TYPES)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    thickness = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Angle'
        verbose_name_plural = 'Angles'

class PipeMaterial(BaseMaterial):
    PIPE_TYPES = [
        ('SCH', 'Scheduled Pipe'),
        ('SS', 'Pipe Stainless'),
        ('STD', 'Pipe STD'),
        ('XS', 'Pipe XS'),
        ('STL', 'Steel Pipe'),
    ]
    
    pipe_type = models.CharField(max_length=5, choices=PIPE_TYPES)
    diameter = models.DecimalField(max_digits=10, decimal_places=2)
    thickness = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    schedule = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Pipe'
        verbose_name_plural = 'Pipes'

class TubeMaterial(BaseMaterial):
    TUBE_TYPES = [
        ('REC', 'Rectangular Tube'),
        ('SQ', 'Square Tube'),
    ]
    
    tube_type = models.CharField(max_length=5, choices=TUBE_TYPES)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    thickness = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Tube'
        verbose_name_plural = 'Tubes'

class PurlinMaterial(BaseMaterial):
    PURLIN_TYPES = [
        ('C', 'C Purlin'),
        ('Z', 'Z Purlin'),
    ]
    
    purlin_type = models.CharField(max_length=5, choices=PURLIN_TYPES)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    thickness = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    lip = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Purlin'
        verbose_name_plural = 'Purlins'

class BarMaterial(BaseMaterial):
    BAR_TYPES = [
        ('FLAT', 'Flat Bar'),
        ('ROUND', 'Round Bar'),
        ('SQUARE', 'Square Bar'),
    ]
    
    bar_type = models.CharField(max_length=10, choices=BAR_TYPES)
    diameter = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # for round bars
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)    # for flat/square bars
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)     # for flat bars
    length = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Bar'
        verbose_name_plural = 'Bars'

class FastenerMaterial(BaseMaterial):
    FASTENER_TYPES = [
        ('ABOLT', 'Anchor Bolt'),
        ('FWASH', 'Flat Washer'),
        ('TROD', 'Threaded Rod'),
        ('HNUT', 'Hex Nut'),
        ('HBOLT', 'Hex Bolt'),
        ('SSTUD', 'Shear Stud'),
        ('SANCH', 'Stud Anchor'),
    ]
    
    fastener_type = models.CharField(max_length=10, choices=FASTENER_TYPES)
    diameter = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    thread_size = models.CharField(max_length=50, null=True, blank=True)
    finish = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Fastener'
        verbose_name_plural = 'Fasteners'

class PanelMaterial(BaseMaterial):
    PANEL_TYPES = [
        ('DECK', 'Deck Panel'),
        ('ROOF', 'Roof Panel'),
    ]
    
    panel_type = models.CharField(max_length=10, choices=PANEL_TYPES)
    thickness = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    profile_height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Panel'
        verbose_name_plural = 'Panels'

class MiscMaterial(BaseMaterial):
    MISC_TYPES = [
        ('WELD', 'Welding Electrode'),
        ('GRAT', 'Steel Grating'),
        ('ZINC', 'Zinc EGI'),
        ('COIL', 'GI Coil'),
        ('ELBOW', 'Elbows'),
        ('FLANGE', 'Flanges'),
    ]
    
    misc_type = models.CharField(max_length=10, choices=MISC_TYPES)

    class Meta:
        verbose_name = 'Miscellaneous Material'
        verbose_name_plural = 'Miscellaneous Materials'

class MaterialProperty(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
        verbose_name = 'Material Property'
        verbose_name_plural = 'Material Properties'
