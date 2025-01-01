from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from django.core.validators import MinValueValidator
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

# Create your models here.

class Material(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilograms'),
        ('m', 'Meters'),
        ('pcs', 'Pieces'),
        ('l', 'Liters'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class ProductionProcess(models.Model):
    CATEGORY_CHOICES = [
        ('PRODUCTION', 'Production'),
        ('QC', 'Quality Control'),
        ('DISPATCH', 'Dispatch'),
        ('SITE', 'Site'),
        ('ENGINEERING', 'Engineering'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='PRODUCTION')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_category_display()} - {self.name}"

    class Meta:
        verbose_name = "Process"
        verbose_name_plural = "Processes"
        ordering = ['category', 'name']

class Project(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]

    INCOTERM_CHOICES = [
        ('EXW', 'Ex Works'),
        ('FOB', 'Free on Board'),
        ('CIF', 'Cost, Insurance, and Freight'),
        ('DDP', 'Delivered Duty Paid'),
    ]

    STRUCTURE_TYPE_CHOICES = [
        ('INDUSTRIAL', 'Industrial Building'),
        ('COMMERCIAL', 'Commercial Building'),
        ('RESIDENTIAL', 'Residential Building'),
        ('WAREHOUSE', 'Warehouse'),
        ('OTHER', 'Other'),
    ]

    PROJECT_NATURE_CHOICES = [
        ('NEW', 'New Construction'),
        ('EXPANSION', 'Expansion'),
        ('RENOVATION', 'Renovation'),
        ('MAINTENANCE', 'Maintenance'),
    ]

    WELDING_PROCESS_CHOICES = [
        ('SMAW', 'Shielded Metal Arc Welding'),
        ('GMAW', 'Gas Metal Arc Welding'),
        ('FCAW', 'Flux Cored Arc Welding'),
        ('SAW', 'Submerged Arc Welding'),
    ]

    # Basic Information
    estimation_number = models.CharField(max_length=20, unique=True, verbose_name='Estimation #', default='EST-000')
    project_number = models.CharField(max_length=50, unique=True, verbose_name='Project #', help_text='Project number (e.g., PRJ-2024-001)', db_index=True)
    name = models.CharField(max_length=255, verbose_name='Project Name')
    project_manager = models.CharField(max_length=100, verbose_name='Project Manager', null=True, blank=True)
    client_name = models.CharField(max_length=100, verbose_name='Client Name')
    
    # Contract Dates
    contract_date = models.DateField(null=True, blank=True, verbose_name='Contract Date')
    down_payment_date = models.DateField(null=True, blank=True, verbose_name='Down Payment Date')
    
    # Project Details
    structure_type = models.CharField(max_length=50, choices=STRUCTURE_TYPE_CHOICES, verbose_name='Structure Type', default='INDUSTRIAL')
    number_of_structures = models.IntegerField(verbose_name='No. of structures', default=1)
    erection_subcontractor = models.CharField(max_length=100, verbose_name='Erection Subcontractor', blank=True)
    
    # Payments
    down_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Down Payment')
    down_payment_ack = models.BooleanField(default=False, verbose_name='Down Payment Ack')
    payment_2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Payment 2')
    payment_2_ack = models.BooleanField(default=False, verbose_name='Payment 2 Ack')
    payment_3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Payment 3')
    payment_3_ack = models.BooleanField(default=False, verbose_name='Payment 3 Ack')
    payment_4 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Payment 4')
    payment_4_ack = models.BooleanField(default=False, verbose_name='Payment 4 Ack')
    payment_5 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Payment 5')
    payment_5_ack = models.BooleanField(default=False, verbose_name='Payment 5 Ack')
    
    # Retentions
    preliminary_retention = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Preliminary Retention')
    ho_retention = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='H.O Retention')
    
    # Contract Details
    incoterm = models.CharField(max_length=20, choices=INCOTERM_CHOICES, verbose_name='Incoterm', default='EXW')
    scope_of_work = models.TextField(verbose_name='Scope of Work', default='')
    project_nature = models.CharField(max_length=20, choices=PROJECT_NATURE_CHOICES, verbose_name='Project Nature', default='NEW')
    
    # Technical Details
    contractual_tonnage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Contractual Tonnage', default=0)
    engineering_tonnage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Engineering Tonnage')
    galvanized = models.BooleanField(default=False, verbose_name='Galvanized')
    galvanization_microns = models.IntegerField(null=True, blank=True, verbose_name='Galvanization Microns')
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Area', default=0)
    m2_per_ton = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='m2/Ton', default=0)
    
    # Paint Details
    paint_coat_1 = models.CharField(max_length=100, null=True, blank=True, verbose_name='Paint Coat 1')
    coat_1_microns = models.IntegerField(null=True, blank=True, verbose_name='Coat 1 - Microns')
    coat_1_liters_needed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Liters Needed')
    
    paint_coat_2 = models.CharField(max_length=100, null=True, blank=True, verbose_name='Paint Coat 2')
    coat_2_microns = models.IntegerField(null=True, blank=True, verbose_name='Coat 2 - Microns')
    coat_2_liters_needed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Liters Needed')
    
    paint_coat_3 = models.CharField(max_length=100, null=True, blank=True, verbose_name='Paint Coat 3')
    coat_3_microns = models.IntegerField(null=True, blank=True, verbose_name='Coat 3 - Microns')
    coat_3_liters_needed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Liters Needed')
    
    paint_coat_4 = models.CharField(max_length=100, null=True, blank=True, verbose_name='Paint Coat 4')
    coat_4_microns = models.IntegerField(null=True, blank=True, verbose_name='Coat 4 - Microns')
    coat_4_liters_needed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Liters Needed')
    
    top_coat_ral_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='Top Coat RAL Number')
    
    # Welding Details
    welding_process = models.CharField(max_length=20, choices=WELDING_PROCESS_CHOICES, verbose_name='Welding Process', default='SMAW')
    welding_wire_aws_class = models.CharField(max_length=50, verbose_name='Welding Wire AWS Class', default='')
    pqr_no = models.CharField(max_length=50, verbose_name='PQR NO', default='')
    wps_no = models.CharField(max_length=50, verbose_name='WPS NO', default='')
    standard_code = models.CharField(max_length=50, verbose_name='Standard Code', default='')
    
    # Status and Timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Project {self.project_number} - {self.name}"

    def get_production_stats(self):
        from django.db.models import Sum, Count, F, Q, DecimalField
        from django.db.models.functions import Coalesce

        # Get raw data totals
        raw_data = RawData.objects.filter(project_number=self.project_number)
        total_quantity = raw_data.aggregate(
            total=Coalesce(Sum('net_weight_total'), 0, output_field=DecimalField())
        )['total']
        total_items = raw_data.count()

        # Get production logs
        production_logs = ProductionLog.objects.filter(project_number=self.project_number)
        total_produced = production_logs.aggregate(
            total=Coalesce(Sum('produced_quantity'), 0, output_field=DecimalField())
        )['total']

        # Get completed items by comparing log_designation totals
        log_totals = {}
        for log in production_logs:
            if log.log_designation not in log_totals:
                log_totals[log.log_designation] = 0
            log_totals[log.log_designation] += float(log.produced_quantity)

        completed_items = 0
        for data in raw_data:
            if data.log_designation in log_totals:
                if log_totals[data.log_designation] >= float(data.net_weight_total):
                    completed_items += 1

        # Calculate progress (convert to float for percentage calculation)
        progress = float(total_produced / total_quantity * 100) if total_quantity > 0 else 0

        return {
            'total_quantity': total_quantity,
            'total_produced': total_produced,
            'total_items': total_items,
            'completed_count': completed_items,
            'progress': round(progress, 2)
        }

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['project_number']

class Building(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    
    # Internal relation using Project's id
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='buildings'
    )
    name = models.CharField(
        max_length=100, 
        help_text='Building name (e.g., "Building A", "Building B")',
        default='Building A'
    )
    description = models.TextField(blank=True, null=True)
    
    # Design Dates
    design_start_date = models.DateField(null=True, blank=True, verbose_name='Design Start Date')
    design_end_date = models.DateField(null=True, blank=True, verbose_name='Design End Date')
    shop_drawing_start_date = models.DateField(null=True, blank=True, verbose_name='Shop Drawing Start Date')
    shop_drawing_end_date = models.DateField(null=True, blank=True, verbose_name='Shop Drawing End Date')
    planned_start_date = models.DateField(null=True, blank=True, verbose_name='Production Start Date')
    planned_end_date = models.DateField(null=True, blank=True, verbose_name='Production End Date')
    actual_start_date = models.DateField(null=True, blank=True, verbose_name='Actual Production Start')
    actual_end_date = models.DateField(null=True, blank=True, verbose_name='Actual Production End')
    
    # QC Information
    qc_inspection_date = models.DateField(null=True, blank=True, verbose_name='QC Inspection Date')
    qc_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Inspection'),
            ('passed', 'Passed'),
            ('failed', 'Failed'),
            ('conditional', 'Conditional Pass')
        ],
        default='pending',
        verbose_name='QC Status'
    )
    qc_remarks = models.TextField(blank=True, null=True, verbose_name='QC Remarks')
    
    # Building Information
    tonnage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Tonnage',
        help_text='Total tonnage for this building'
    )
    area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Area (m²)',
        help_text='Total area of the building in square meters'
    )
    
    # Status and Progress
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started', verbose_name='Status')
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Progress (%)')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Building"
        verbose_name_plural = "Buildings"
        ordering = ['project__project_number', 'name']
        unique_together = ['project', 'name']

    def __str__(self):
        return f"{self.project.project_number} - {self.name}"

    @property
    def project_number(self):
        return self.project.project_number if self.project else None

class RawData(models.Model):
    row_id = models.CharField(
        max_length=255, 
        unique=True, 
        verbose_name="Row ID",
        editable=False,
        null=True,
        blank=True
    )
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='rawdata'
    )
    project_number = models.CharField(
        max_length=50, 
        db_index=True,
        default=''
    )
    building = models.ForeignKey(
        Building, 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='rawdata'
    )
    building_name = models.CharField(
        max_length=100,
        verbose_name="Building Name",
        null=True,
        blank=True
    )
    log_designation = models.CharField(
        max_length=255,
        verbose_name="Log Designation"
    )
    part_designation = models.CharField(
        max_length=255,
        verbose_name="Part Designation"
    )
    assembly_mark = models.CharField(
        max_length=255,
        verbose_name="Assembly Mark"
    )
    part_mark = models.CharField(
        max_length=255,
        verbose_name="Part Mark"
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Part name or description"
    )
    quantity = models.IntegerField(
        verbose_name="Quantity",
        validators=[MinValueValidator(0)]
    )
    profile = models.CharField(
        max_length=255,
        verbose_name="Profile"
    )
    grade = models.CharField(
        max_length=255,
        verbose_name="Grade"
    )
    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Length(mm)",
        validators=[MinValueValidator(0)]
    )
    net_area_single = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Net Area(m²)",
        validators=[MinValueValidator(0)]
    )
    net_area_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Net Area(m²) for all",
        help_text="Total area from raw data",
        validators=[MinValueValidator(0)]
    )
    single_part_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Single Part Weight",
        validators=[MinValueValidator(0)]
    )
    net_weight_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Net Weight(kg) for all",
        help_text="Total weight from raw data",
        validators=[MinValueValidator(0)]
    )
    revision = models.CharField(
        max_length=20,
        verbose_name="Revision#"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'log_designation']),
            models.Index(fields=['building', 'assembly_mark']),
        ]

    def __str__(self):
        return f"{self.project_number} - {self.log_designation}"

    def save(self, *args, **kwargs):
        if self.project and not self.project_number:
            self.project_number = self.project.project_number
            if not self.row_id:
                self.row_id = f"{self.project_number}_{self.log_designation}_{self.assembly_mark}_{self.part_mark}"
        super().save(*args, **kwargs)

class Facility(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Facilities"
        ordering = ['name']

class ProductionTeam(models.Model):
    name = models.CharField(max_length=100)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='teams', null=True)
    team_leader = models.ForeignKey('Personnel', on_delete=models.SET_NULL, null=True, blank=True, related_name='led_teams')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.facility})"

    class Meta:
        unique_together = ['name', 'facility']
        ordering = ['facility', 'name']

class Personnel(models.Model):
    ROLE_CHOICES = [
        ('WORKER', 'Worker'),
        ('TEAM_LEADER', 'Team Leader'),
        ('SUPERVISOR', 'Supervisor'),
        ('MANAGER', 'Manager'),
    ]

    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='WORKER')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='personnel', null=True, blank=True)
    team = models.ForeignKey(ProductionTeam, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "Personnel"
        ordering = ['facility', 'last_name', 'first_name']

class ProductionLog(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='production_logs',
        null=True,
        blank=True
    )
    project_number = models.CharField(max_length=50, db_index=True, default='')
    log_designation = models.CharField(max_length=100)
    process = models.ForeignKey(ProductionProcess, on_delete=models.PROTECT)
    production_date = models.DateField()
    produced_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)
    team = models.ForeignKey(ProductionTeam, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-production_date']
        verbose_name = "Production Log"
        verbose_name_plural = "Production Logs"

    def __str__(self):
        return f"{self.project_number} - {self.log_designation} ({self.production_date})"

    def save(self, *args, **kwargs):
        if self.project and not self.project_number:
            self.project_number = self.project.project_number
        super().save(*args, **kwargs)

class QualityCheck(models.Model):
    RESULT_CHOICES = [
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('pending', 'Pending Review'),
    ]
    
    production_log = models.ForeignKey(ProductionLog, on_delete=models.CASCADE)
    raw_data = models.ForeignKey(RawData, on_delete=models.SET_NULL, null=True, blank=True)
    inspector = models.ForeignKey(User, on_delete=models.CASCADE)
    check_time = models.DateTimeField(auto_now_add=True)
    parameter = models.CharField(max_length=255)
    measurement = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    specification_min = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    specification_max = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    result = models.CharField(max_length=20, choices=RESULT_CHOICES)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.production_log} - {self.parameter} ({self.result})"

    def save(self, *args, **kwargs):
        if not self.raw_data and self.production_log and self.production_log.raw_data:
            self.raw_data = self.production_log.raw_data
        super().save(*args, **kwargs)

class MaterialUsage(models.Model):
    production_log = models.ForeignKey(ProductionLog, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity_used = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.production_log} - {self.material.name} ({self.quantity_used} {self.material.unit})"

    def clean(self):
        if self.quantity_used > self.material.quantity:
            raise ValidationError(
                f"Not enough {self.material.name} in stock. Available: {self.material.quantity} {self.material.unit}"
            )
