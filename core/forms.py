from django import forms
from django.core.exceptions import ValidationError
from .models import (Material, ProductionProcess, Project, ProductionLog, QualityCheck, 
                    MaterialUsage, RawData, ProductionTeam, Building)
from datetime import date

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
    class Meta:
        model = Building
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Building A'}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'})
        }

BuildingFormSet = forms.inlineformset_factory(
    Project, Building,
    form=BuildingForm,
    fields=['name', 'description'],
    extra=1,
    can_delete=True
)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_number', 'name', 'client_name', 'status']
        widgets = {
            'project_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1001'}),
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
    project_number = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    log_designation = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = ProductionLog
        fields = [
            'project_number', 'log_designation', 'process', 'production_date',
            'produced_quantity', 'facility', 'team', 'status'
        ]
        widgets = {
            'production_date': forms.DateInput(attrs={'type': 'date'}),
            'produced_quantity': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get unique project numbers from raw data
        projects = RawData.objects.values_list('project_number', flat=True).distinct()
        self.fields['project_number'].choices = [('', '-- Select Project --')] + [(p, p) for p in sorted(projects) if p]
        
        # Initialize log designation choices as empty
        self.fields['log_designation'].choices = [('', '-- Select Log Designation --')]
        
        # If project number is in the data, load its log designations
        if 'project_number' in self.data:
            project_number = self.data.get('project_number')
            log_designations = RawData.objects.filter(
                project_number=project_number
            ).values_list('log_designation', flat=True).distinct()
            self.fields['log_designation'].choices += [(l, l) for l in sorted(log_designations) if l]
        
        # If we're editing an existing instance, load its log designations
        elif self.instance.pk:
            project_number = self.instance.project_number
            log_designations = RawData.objects.filter(
                project_number=project_number
            ).values_list('log_designation', flat=True).distinct()
            self.fields['log_designation'].choices += [(l, l) for l in sorted(log_designations) if l]
        
        # Initialize team choices
        self.fields['team'].queryset = ProductionTeam.objects.none()
        
        if 'facility' in self.data:
            try:
                facility_id = int(self.data.get('facility'))
                self.fields['team'].queryset = ProductionTeam.objects.filter(facility_id=facility_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.facility:
            self.fields['team'].queryset = self.instance.facility.teams.all()

    def clean(self):
        cleaned_data = super().clean()
        project_number = cleaned_data.get('project_number')
        log_designation = cleaned_data.get('log_designation')
        facility = cleaned_data.get('facility')
        team = cleaned_data.get('team')
        produced_quantity = cleaned_data.get('produced_quantity')

        if facility and team and team.facility != facility:
            raise forms.ValidationError("Selected team does not belong to the selected facility.")

        if produced_quantity is not None and produced_quantity < 0:
            raise forms.ValidationError("Produced quantity cannot be negative.")

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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs and 'production_log' in kwargs['initial']:
            self.fields['production_log'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        material = cleaned_data.get('material')
        quantity_used = cleaned_data.get('quantity_used')

        if material and quantity_used:
            if quantity_used > material.quantity:
                raise forms.ValidationError(
                    f"Not enough {material.name} in stock. Available: {material.quantity} {material.unit}"
                )
        if quantity_used is not None and quantity_used < 0:
            self.add_error('quantity_used', 'Value cannot be negative.')
        return cleaned_data

class RawDataForm(forms.ModelForm):
    class Meta:
        model = RawData
        fields = [
            'project', 'building', 'building_name', 'log_designation', 
            'part_designation', 'assembly_mark', 'part_mark', 'name', 'quantity', 
            'profile', 'grade', 'length', 'net_area_single', 'net_area_total',
            'single_part_weight', 'net_weight_total', 'revision'
        ]
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'building': forms.Select(attrs={'class': 'form-control'}),
            'building_name': forms.TextInput(attrs={'class': 'form-control'}),
            'log_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'part_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'assembly_mark': forms.TextInput(attrs={'class': 'form-control'}),
            'part_mark': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'profile': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'net_area_single': forms.NumberInput(attrs={'class': 'form-control'}),
            'net_area_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'single_part_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'net_weight_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'revision': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If we have an instance with a project, filter buildings by that project
        if self.instance and self.instance.project:
            self.fields['building'].queryset = Building.objects.filter(project=self.instance.project)
        else:
            self.fields['building'].queryset = Building.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')
        building = cleaned_data.get('building')

        if building and project and building.project != project:
            raise forms.ValidationError("Selected building does not belong to the selected project.")

        return cleaned_data
