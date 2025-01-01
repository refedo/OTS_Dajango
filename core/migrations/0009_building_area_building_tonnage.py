# Generated by Django 5.1.4 on 2025-01-01 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_project_project_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='area',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Total area of the building in square meters', max_digits=10, null=True, verbose_name='Area (m²)'),
        ),
        migrations.AddField(
            model_name='building',
            name='tonnage',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Total tonnage for this building', max_digits=10, null=True, verbose_name='Tonnage'),
        ),
    ]