import pandas as pd
import numpy as np
import logging
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RawDataImportForm
from .models import RawData, Building

logger = logging.getLogger(__name__)

class RawDataImportView(LoginRequiredMixin, FormView):
    template_name = 'core/import_raw_data.html'
    form_class = RawDataImportForm
    success_url = '/raw-data/'

    def clean_value(self, value, default=''):
        """Clean pandas value, handling NaN and None"""
        if pd.isna(value):
            return default
        return str(value).strip()

    def clean_float(self, value, default=0.0):
        """Clean pandas float value, handling NaN and None"""
        if pd.isna(value):
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    def form_valid(self, form):
        file = form.cleaned_data['file']
        project = form.cleaned_data['project']
        
        try:
            # Read the file based on its extension
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
                logger.info(f"Reading CSV file: {file.name}")
            else:
                df = pd.read_excel(file)
                logger.info(f"Reading Excel file: {file.name}")

            logger.info(f"File columns: {df.columns.tolist()}")

            # Validate required columns
            required_columns = [
                'building_name', 'log_designation', 'part_designation',
                'assembly_mark', 'part_mark', 'name_designation', 'quantity',
                'profile', 'grade', 'length', 'net_area_single',
                'net_area_total', 'single_part_weight', 'net_weight_total',
                'revision'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                error_msg = f'Missing required columns: {", ".join(missing_columns)}'
                logger.error(error_msg)
                messages.error(self.request, error_msg)
                return self.form_invalid(form)

            # Process each row
            success_count = 0
            error_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Get or create building
                    building_name = self.clean_value(row['building_name'])
                    building, _ = Building.objects.get_or_create(
                        project=project,
                        name=building_name,
                        defaults={'description': f'Imported: {building_name}'}
                    )

                    # Get values from the file
                    part_designation = self.clean_value(row['part_designation'])
                    name_designation = self.clean_value(row['name_designation'])

                    # Create raw data entry
                    RawData.objects.create(
                        project=project,
                        project_number=project.project_number,
                        building=building,
                        building_name=building_name,
                        log_designation=self.clean_value(row['log_designation']),
                        part_designation=part_designation,
                        assembly_mark=self.clean_value(row['assembly_mark']),
                        part_mark=self.clean_value(row['part_mark']),
                        name_designation=name_designation,
                        quantity=int(self.clean_float(row['quantity'], 0)),
                        profile=self.clean_value(row['profile']),
                        grade=self.clean_value(row['grade']),
                        length=self.clean_float(row['length'], 0),
                        net_area_single=self.clean_float(row['net_area_single'], 0),
                        net_area_total=self.clean_float(row['net_area_total'], 0),
                        single_part_weight=self.clean_float(row['single_part_weight'], 0),
                        net_weight_total=self.clean_float(row['net_weight_total'], 0),
                        revision=self.clean_value(row['revision'])
                    )
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    error_msg = f"Error in row {index + 2}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    continue

            if success_count > 0:
                messages.success(
                    self.request,
                    f'Successfully imported {success_count} records. '
                    f'Failed to import {error_count} records.'
                )
            else:
                error_details = '\n'.join(errors[:5])  # Show first 5 errors
                messages.error(
                    self.request,
                    f'No records were imported. Please check your file format.\n'
                    f'Errors encountered:\n{error_details}'
                )

        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            messages.error(self.request, f'Error processing file: {str(e)}')
            return self.form_invalid(form)

        return super().form_valid(form)
