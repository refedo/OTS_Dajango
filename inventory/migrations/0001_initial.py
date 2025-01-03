# Generated by Django 5.1.4 on 2025-01-03 19:23

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AngleMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(max_length=50)),
                ('grade', models.CharField(blank=True, max_length=50, null=True)),
                ('standard', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True)),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('minimum_stock', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('angle_type', models.CharField(choices=[('EQ', 'Equal Angle'), ('UEQ', 'UnEqual Angle')], max_length=5)),
                ('height', models.DecimalField(decimal_places=2, max_digits=10)),
                ('width', models.DecimalField(decimal_places=2, max_digits=10)),
                ('thickness', models.DecimalField(decimal_places=2, max_digits=10)),
                ('length', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'Angle',
                'verbose_name_plural': 'Angles',
            },
        ),
        migrations.CreateModel(
            name='BarMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(max_length=50)),
                ('grade', models.CharField(blank=True, max_length=50, null=True)),
                ('standard', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True)),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('minimum_stock', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bar_type', models.CharField(choices=[('FLAT', 'Flat Bar'), ('ROUND', 'Round Bar'), ('SQUARE', 'Square Bar')], max_length=10)),
                ('diameter', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('width', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('length', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'Bar',
                'verbose_name_plural': 'Bars',
            },
        ),
        migrations.CreateModel(
            name='BeamMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(max_length=50)),
                ('grade', models.CharField(blank=True, max_length=50, null=True)),
                ('standard', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True)),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('minimum_stock', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('beam_type', models.CharField(choices=[('IPE-AA', 'IPE-AA Beam'), ('HEA', 'HEA Beam'), ('HEB', 'HEB Beam'), ('IPE', 'IPE Beam'), ('JIS', 'JIS Beam'), ('UB', 'UB Beam'), ('UPE', 'UPE Beam'), ('UPN', 'UPN Beam'), ('W', 'W Section')], max_length=10)),
                ('height', models.DecimalField(decimal_places=2, max_digits=10)),
                ('width', models.DecimalField(decimal_places=2, max_digits=10)),
                ('flange_thickness', models.DecimalField(decimal_places=2, max_digits=10)),
                ('web_thickness', models.DecimalField(decimal_places=2, max_digits=10)),
                ('length', models.DecimalField(decimal_places=2, max_digits=10)),
                ('weight_per_meter', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'Beam',
                'verbose_name_plural': 'Beams',
            },
        ),
        migrations.CreateModel(
            name='FastenerMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(max_length=50)),
                ('grade', models.CharField(blank=True, max_length=50, null=True)),
                ('standard', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True)),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('minimum_stock', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fastener_type', models.CharField(choices=[('ABOLT', 'Anchor Bolt'), ('FWASH', 'Flat Washer'), ('TROD', 'Threaded Rod'), ('HNUT', 'Hex Nut'), ('HBOLT', 'Hex Bolt'), ('SSTUD', 'Shear Stud'), ('SANCH', 'Stud Anchor')], max_length=10)),
                ('diameter', models.DecimalField(decimal_places=2, max_digits=10)),
                ('length', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('thread_size', models.CharField(blank=True, max_length=50, null=True)),
                ('finish', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Fastener',
                'verbose_name_plural': 'Fasteners',
            },
        ),
        migrations.CreateModel(
            name='MiscMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(max_length=50)),
                ('grade', models.CharField(blank=True, max_length=50, null=True)),
                ('standard', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True)),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('minimum_stock', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('misc_type', models.CharField(choices=[('WELD', 'Welding Electrode'), ('GRAT', 'Steel Grating'), ('ZINC', 'Zinc EGI'), ('COIL', 'GI Coil'), ('ELBOW', 'Elbows'), ('FLANGE', 'Flanges')], max_length=10)),
            ],
            options={
                'verbose_name': 'Miscellaneous Material',
                'verbose_name_plural': 'Miscellaneous Materials',
            },
        ),
        migrations.CreateModel(
            name='PanelMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(max_length=50)),
                ('grade', models.CharField(blank=True, max_length=50, null=True)),
                ('standard', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True)),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('minimum_stock', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('panel_type', models.CharField(choices=[('DECK', 'Deck Panel'), ('ROOF', 'Roof Panel')], max_length=10)),
                ('thickness', models.DecimalField(decimal_places=2, max_digits=10)),
                ('width', models.DecimalField(decimal_places=2, max_digits=10)),
                ('length', models.DecimalField(decimal_places=2, max_digits=10)),
                ('profile_height', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'verbose_name': 'Panel',
                'verbose_name_plural': 'Panels',
            },
        ),
        migrations.CreateModel(
            name='PipeMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(max_length=50)),
                ('grade', models.CharField(blank=True, max_length=50, null=True)),
                ('standard', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True)),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('minimum_stock', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pipe_type', models.CharField(choices=[('SCH', 'Scheduled Pipe'), ('SS', 'Pipe Stainless'), ('STD', 'Pipe STD'), ('XS', 'Pipe XS'), ('STL', 'Steel Pipe')], max_length=5)),
                ('diameter', models.DecimalField(decimal_places=2, max_digits=10)),
                ('thickness', models.DecimalField(decimal_places=2, max_digits=10)),
                ('length', models.DecimalField(decimal_places=2, max_digits=10)),
                ('schedule', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Pipe',
                'verbose_name_plural': 'Pipes',
            },
        ),
        migrations.CreateModel(
            name='PurlinMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(max_length=50)),
                ('grade', models.CharField(blank=True, max_length=50, null=True)),
                ('standard', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True)),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('minimum_stock', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('purlin_type', models.CharField(choices=[('C', 'C Purlin'), ('Z', 'Z Purlin')], max_length=5)),
                ('height', models.DecimalField(decimal_places=2, max_digits=10)),
                ('width', models.DecimalField(decimal_places=2, max_digits=10)),
                ('thickness', models.DecimalField(decimal_places=2, max_digits=10)),
                ('length', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lip', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'verbose_name': 'Purlin',
                'verbose_name_plural': 'Purlins',
            },
        ),
        migrations.CreateModel(
            name='SheetMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(max_length=50)),
                ('grade', models.CharField(blank=True, max_length=50, null=True)),
                ('standard', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True)),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('minimum_stock', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sheet_type', models.CharField(choices=[('AL', 'Aluminum Sheet'), ('BLK', 'Black Sheet'), ('CHK', 'Checkered Plate'), ('GI', 'GI Sheet'), ('SS', 'Stainless Steel Sheet')], max_length=10)),
                ('thickness', models.DecimalField(decimal_places=2, max_digits=10)),
                ('width', models.DecimalField(decimal_places=2, max_digits=10)),
                ('length', models.DecimalField(decimal_places=2, max_digits=10)),
                ('surface_treatment', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Sheet',
                'verbose_name_plural': 'Sheets',
            },
        ),
        migrations.CreateModel(
            name='TubeMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('unit', models.CharField(max_length=50)),
                ('grade', models.CharField(blank=True, max_length=50, null=True)),
                ('standard', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True)),
                ('quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('minimum_stock', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tube_type', models.CharField(choices=[('REC', 'Rectangular Tube'), ('SQ', 'Square Tube')], max_length=5)),
                ('height', models.DecimalField(decimal_places=2, max_digits=10)),
                ('width', models.DecimalField(decimal_places=2, max_digits=10)),
                ('thickness', models.DecimalField(decimal_places=2, max_digits=10)),
                ('length', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'Tube',
                'verbose_name_plural': 'Tubes',
            },
        ),
        migrations.CreateModel(
            name='MaterialProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=255)),
                ('unit', models.CharField(blank=True, max_length=50)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Material Property',
                'verbose_name_plural': 'Material Properties',
                'indexes': [models.Index(fields=['content_type', 'object_id'], name='inventory_m_content_fe952f_idx')],
            },
        ),
    ]
