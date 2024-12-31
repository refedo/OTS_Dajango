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
    
    # Internal identifier (won't be used in business logic)
    id = models.BigAutoField(primary_key=True)
    
    # Business identifier (used everywhere in the system)
    project_number = models.CharField(
        max_length=10, 
        unique=True, 
        verbose_name='Project #',
        help_text='Project number (e.g., 1001)',
        db_index=True  # Add index for faster lookups
    )
    
    name = models.CharField(max_length=255, verbose_name='Project Name')
    client_name = models.CharField(max_length=100, verbose_name='Client Name')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Project {self.project_number} - {self.name}"

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['project_number']

class Building(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Display using project_number
        return f"Project {self.project.project_number} - {self.name}"

    @property
    def project_number(self):
        # Convenience property to get project_number
        return self.project.project_number

    class Meta:
        verbose_name = "Building"
        verbose_name_plural = "Buildings"
        ordering = ['project__project_number', 'name']  # Order by project_number then building name
        unique_together = ['project', 'name']

class RawData(models.Model):
    row_id = models.CharField(max_length=255, unique=True, verbose_name="Row ID", editable=False, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, null=True, blank=True)
    building_name = models.CharField(max_length=100, verbose_name="Building Name", null=True, blank=True)
    log_designation = models.CharField(max_length=255, verbose_name="Log Designation")
    part_designation = models.CharField(max_length=255, verbose_name="Part Designation")
    assembly_mark = models.CharField(max_length=255, verbose_name="Assembly Mark")
    part_mark = models.CharField(max_length=255, verbose_name="Part Mark")
    name = models.CharField(max_length=255, blank=True, help_text="Part name or description")
    quantity = models.IntegerField(verbose_name="Quantity", validators=[MinValueValidator(0)])
    profile = models.CharField(max_length=255, verbose_name="Profile")
    grade = models.CharField(max_length=255, verbose_name="Grade")
    length = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Length(mm)", validators=[MinValueValidator(0)])
    net_area_single = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Net Area(m²)", validators=[MinValueValidator(0)])
    net_area_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Net Area(m²) for all", help_text="Total area from raw data", validators=[MinValueValidator(0)])
    single_part_weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Single Part Weight", validators=[MinValueValidator(0)])
    net_weight_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Net Weight(kg) for all", help_text="Total weight from raw data", validators=[MinValueValidator(0)])
    revision = models.CharField(max_length=20, verbose_name="Revision#")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.project_number if self.project else ''} - {self.log_designation} - {self.assembly_mark}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'log_designation']),
            models.Index(fields=['building', 'assembly_mark']),
        ]

    def save(self, *args, **kwargs):
        if self.project:
            # Add project number to the row_id for uniqueness
            if not self.row_id:
                self.row_id = f"{self.project.project_number}_{self.log_designation}_{self.assembly_mark}_{self.part_mark}"
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

    # Use Project relationship instead of project_number
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='production_logs',
        null=True,  # Allow null temporarily for migration
        blank=True
    )
    log_designation = models.CharField(max_length=100)
    process = models.ForeignKey(ProductionProcess, on_delete=models.PROTECT)
    production_date = models.DateField()
    produced_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)
    team = models.ForeignKey(ProductionTeam, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)  # Keep nullable for now
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.project:
            return f"{self.project.project_number} - {self.log_designation} - {self.process}"
        return f"{self.log_designation} - {self.process}"

    @property
    def project_number(self):
        # Convenience property to get project_number
        return self.project.project_number if self.project else None

    class Meta:
        ordering = ['-production_date']
        verbose_name = "Production Log"
        verbose_name_plural = "Production Logs"

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
            # Link to the same raw data as the production log
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
