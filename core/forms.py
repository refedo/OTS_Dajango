from django import forms
from django.core.exceptions import ValidationError
from .models import (Material, ProductionProcess, Project, ProductionLog, QualityCheck, 
                    MaterialUsage, RawData, ProductionTeam, Building)
from datetime import date
import re

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['code', 'name', 'description', 'unit', 'quantity', 'minimum_stock']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'code': forms.TextInput(attrs={'class': 'uppercase'}),
            'quantity': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
            'minimum_stock': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        for field in ['quantity', 'minimum_stock']:
            value = cleaned_data.get(field)
            if value is not None and value < 0:
                self.add_error(field, 'Value cannot be negative.')
        return cleaned_data

class ProductionProcessForm(forms.ModelForm):
    class Meta:
        model = ProductionProcess
        fields = ['name', 'category', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BuildingForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data.get('name')
        project = self.cleaned_data.get('project')
        if name and project:
            # Check uniqueness within the same project
            if Building.objects.filter(
                project=project,
                name__iexact=name
            ).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise ValidationError('This building name already exists in the project.')
        return name.strip()

    class Meta:
        model = Building
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., A1, Block B, Tower 1'
            }),
            'description': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control'
            })
        }

BuildingFormSet = forms.inlineformset_factory(
    Project, Building,
    form=BuildingForm,
    fields=['name', 'description'],
    extra=1,
    can_delete=True
)

class ProjectForm(forms.ModelForm):
    def clean_project_number(self):
        project_number = self.cleaned_data.get('project_number')
        if project_number:
            # Ensure project number follows the standard format PRJ-YYYY-XXX
            if not re.match(r'^PRJ-\d{4}-\d{3}$', project_number):
                raise ValidationError(
                    'Project number must follow the format PRJ-YYYY-XXX '
                    '(e.g., PRJ-2024-001)'
                )
            # Check uniqueness case-insensitive
            if Project.objects.filter(project_number__iexact=project_number).exclude(pk=self.instance.pk).exists():
                raise ValidationError('This project number already exists.')
        return project_number.upper()

    class Meta:
        model = Project
        fields = ['project_number', 'name', 'client_name', 'status']
        widgets = {
            'project_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., PRJ-2024-001',
                'pattern': r'^PRJ-\d{4}-\d{3}$'
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ProjectWithBuildingsForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_number', 'name', 'client_name', 'status']
        widgets = {
            'project_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1001'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ProductionLogForm(forms.ModelForm):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    log_designation = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    team = forms.ModelChoiceField(
        queryset=ProductionTeam.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = ProductionLog
        fields = [
            'project', 'log_designation', 'process', 'production_date',
            'produced_quantity', 'facility', 'team', 'status'
        ]
        widgets = {
            'production_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'produced_quantity': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'process': forms.Select(attrs={'class': 'form-select'}),
            'facility': forms.Select(attrs={'class': 'form-select', 'data-affects': 'team'}),
            'team': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get unique project numbers and their IDs from raw data
        project_choices = Project.objects.filter(
            id__in=RawData.objects.values_list('project', flat=True).distinct()
        )
        self.fields['project'].queryset = project_choices

        # If we have an instance, populate log_designation choices
        if self.instance and self.instance.pk:
            log_choices = RawData.objects.filter(
                project=self.instance.project
            ).values_list('log_designation', 'log_designation').distinct()
            self.fields['log_designation'].choices = [('', '---------')] + list(log_choices)

        # Filter teams based on facility if facility is selected
        if self.instance and self.instance.facility:
            self.fields['team'].queryset = ProductionTeam.objects.filter(facility=self.instance.facility)
        else:
            self.fields['team'].queryset = ProductionTeam.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        production_date = cleaned_data.get('production_date')
        produced_quantity = cleaned_data.get('produced_quantity')

        if production_date and production_date > date.today():
            self.add_error('production_date', 'Production date cannot be in the future.')

        if produced_quantity is not None:
            if produced_quantity <= 0:
                self.add_error('produced_quantity', 'Produced quantity must be greater than zero.')

        return cleaned_data

class QualityCheckForm(forms.ModelForm):
    class Meta:
        model = QualityCheck
        fields = ['production_log', 'parameter', 'measurement',
                 'specification_min', 'specification_max', 'result', 'notes']
        widgets = {
            'production_log': forms.Select(attrs={'class': 'form-control'}),
            'parameter': forms.TextInput(attrs={'class': 'form-control'}),
            'measurement': forms.NumberInput(attrs={'min': '0', 'class': 'form-control', 'step': '0.001'}),
            'specification_min': forms.NumberInput(attrs={'min': '0', 'class': 'form-control', 'step': '0.001'}),
            'specification_max': forms.NumberInput(attrs={'min': '0', 'class': 'form-control', 'step': '0.001'}),
            'result': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        value = cleaned_data.get('measurement')
        if value is not None and value < 0:
            self.add_error('measurement', 'Value cannot be negative.')
        value = cleaned_data.get('specification_min')
        if value is not None and value < 0:
            self.add_error('specification_min', 'Value cannot be negative.')
        value = cleaned_data.get('specification_max')
        if value is not None and value < 0:
            self.add_error('specification_max', 'Value cannot be negative.')
        if 'measurement' in cleaned_data and 'specification_min' in cleaned_data and 'specification_max' in cleaned_data:
            measurement = cleaned_data['measurement']
            spec_min = cleaned_data['specification_min']
            spec_max = cleaned_data['specification_max']
            
            # Auto-set result based on measurement and specifications
            if measurement < spec_min or measurement > spec_max:
                cleaned_data['result'] = 'fail'
            else:
                cleaned_data['result'] = 'pass'
                
        return cleaned_data

class MaterialUsageForm(forms.ModelForm):
    class Meta:
        model = MaterialUsage
        fields = ['production_log', 'material', 'quantity_used']
        widgets = {
            'quantity_used': forms.NumberInput(attrs={'min': '0', 'class': 'form-control', 'step': '0.01'}),
            'material': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs and 'production_log' in kwargs['initial']:
            self.fields['production_log'].widget = forms.HiddenInput()

        # Filter materials to only show those with available stock
        self.fields['material'].queryset = Material.objects.filter(quantity__gt=0)

    def clean(self):
        cleaned_data = super().clean()
        material = cleaned_data.get('material')
        quantity_used = cleaned_data.get('quantity_used')

        if material and quantity_used:
            if quantity_used <= 0:
                self.add_error('quantity_used', 'Quantity used must be greater than zero.')
            elif quantity_used > material.quantity:
                self.add_error('quantity_used', 
                    f'Insufficient stock. Available: {material.quantity} {material.unit}')

            # Check if this would bring stock below minimum level
            remaining_stock = material.quantity - quantity_used
            if remaining_stock < material.minimum_stock:
                self.add_error('quantity_used',
                    f'Warning: This usage will bring stock below minimum level ({material.minimum_stock} {material.unit})')

        return cleaned_data

class RawDataForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')
        building = cleaned_data.get('building')
        building_name = cleaned_data.get('building_name')

        if project:
            # Ensure project number in raw data matches the project
            if project.project_number != cleaned_data.get('project_number'):
                raise ValidationError({
                    'project_number': 'Project number must match the selected project.'
                })

        if building and building_name:
            # Ensure building name in raw data matches the building
            if building.name != building_name:
                raise ValidationError({
                    'building_name': 'Building name must match the selected building.'
                })

        return cleaned_data

    class Meta:
        model = RawData
        fields = [
            'project', 'building', 'log_designation', 'part_designation',
            'assembly_mark', 'part_mark', 'name_designation', 'quantity',
            'profile', 'grade', 'length', 'net_area_single', 'net_area_total',
            'single_part_weight', 'net_weight_total', 'revision'
        ]
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'building': forms.Select(attrs={'class': 'form-control'}),
            'building_name': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'log_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'part_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'assembly_mark': forms.TextInput(attrs={'class': 'form-control'}),
            'part_mark': forms.TextInput(attrs={'class': 'form-control'}),
            'name_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'profile': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'net_area_single': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'net_area_total': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'single_part_weight': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'net_weight_total': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'revision': forms.TextInput(attrs={'class': 'form-control'})
        }

class RawDataImportForm(forms.Form):
    file = forms.FileField(
        label='Select a file',
        help_text='Allowed file types: .xlsx, .xls, .csv',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx,.xls,.csv'})
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        
        if ext not in ['xlsx', 'xls', 'csv']:
            raise ValidationError('Unsupported file type. Please upload an Excel or CSV file.')
        
        return file
