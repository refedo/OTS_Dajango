from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count, F, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.urls import reverse
from .models import (Material, ProductionProcess, Project, ProductionLog, QualityCheck, 
                    MaterialUsage, RawData, Facility, ProductionTeam, Personnel, Building)
from .forms import (MaterialForm, ProductionProcessForm, ProjectForm, ProductionLogForm,
                   QualityCheckForm, MaterialUsageForm, RawDataForm, BuildingFormSet)
from django.utils import timezone
import pandas as pd
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db.models import FloatField

@login_required
def dashboard(request):
    context = {
        'total_materials': Material.objects.count(),
        'total_processes': ProductionProcess.objects.count(),
        'active_projects': Project.objects.filter(status='in_progress').count(),
        'recent_logs': ProductionLog.objects.select_related('process', 'facility', 'team', 'created_by').order_by('-created_at')[:5],
        'low_stock_materials': Material.objects.filter(quantity__lte=F('minimum_stock')),
        'quality_issues': QualityCheck.objects.filter(result='fail').count(),
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def material_list(request):
    materials = Material.objects.all().order_by('code')
    return render(request, 'core/material_list.html', {'materials': materials})

@login_required
def material_create(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save()
            messages.success(request, 'Material created successfully.')
            return redirect('material_detail', pk=material.pk)
    else:
        form = MaterialForm()
    return render(request, 'core/material_form.html', {'form': form, 'title': 'Create Material'})

@login_required
def material_edit(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material updated successfully.')
            return redirect('material_detail', pk=pk)
    else:
        form = MaterialForm(instance=material)
    return render(request, 'core/material_form.html', {'form': form, 'title': 'Edit Material'})

@login_required
def project_list(request):
    projects = Project.objects.all().order_by('-contract_date')
    return render(request, 'core/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        formset = BuildingFormSet(request.POST, instance=Project())
        if form.is_valid() and formset.is_valid():
            project = form.save()
            formset.instance = project
            formset.save()
            messages.success(request, 'Project and buildings created successfully!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
        formset = BuildingFormSet(instance=Project())
    
    return render(request, 'core/project_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Create Project'
    })

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'core/project_form.html', {'form': form, 'title': 'Edit Project'})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        # Store project info for success message
        project_info = f"Project {project.project_number} - {project.name}"
        
        # Delete the project
        project.delete()
        
        messages.success(request, f'{project_info} has been deleted.')
        return redirect('project_list')
    
    context = {
        'project': project,
        'title': 'Delete Project',
    }
    
    return render(request, 'core/project_delete.html', context)

@login_required
def production_list(request):
    production_logs = ProductionLog.objects.all().order_by('-production_date', '-created_at')
    return render(request, 'core/production_list.html', {'production_logs': production_logs})

@login_required
def production_log_create(request):
    # Get search parameters
    search_query = request.GET.get('search', '')
    project_id = request.GET.get('project', '')
    building_name = request.GET.get('building_name', '')
    log_designation = request.GET.get('log_designation', '')

    # Base query for raw data
    raw_data_query = RawData.objects.select_related('project').values(
        'id', 'project__project_number', 'log_designation', 'building_name', 
        'name', 'profile', 'quantity'
    )

    # Get total produced quantities for each log designation
    produced_qty_subquery = ProductionLog.objects.filter(
        project_number=OuterRef('project__project_number'),
        log_designation=OuterRef('log_designation')
    ).values('log_designation').annotate(
        total_produced=Sum('produced_quantity', output_field=FloatField())
    ).values('total_produced')

    # Annotate raw data with produced quantities
    log_items = raw_data_query.annotate(
        produced_quantity=Coalesce(Subquery(produced_qty_subquery), 0.0, output_field=FloatField()),
        remaining_quantity=F('quantity') - Coalesce(Subquery(produced_qty_subquery), 0.0, output_field=FloatField())
    )

    # Apply filters
    if project_id:
        log_items = log_items.filter(project_id=project_id)
    if building_name:
        log_items = log_items.filter(building_name__icontains=building_name)
    if log_designation:
        log_items = log_items.filter(log_designation__icontains=log_designation)
    if search_query:
        log_items = log_items.filter(
            Q(project__project_number__icontains=search_query) |
            Q(building_name__icontains=search_query) |
            Q(log_designation__icontains=search_query) |
            Q(name__icontains=search_query)
        )

    # Only show items with remaining quantity
    log_items = log_items.filter(remaining_quantity__gt=0).order_by(
        'project__project_number', 'building_name', 'log_designation'
    )

    # Get choices for dropdowns
    processes = ProductionProcess.objects.filter(category='PRODUCTION', is_active=True)
    facilities = Facility.objects.filter(is_active=True)
    teams = ProductionTeam.objects.filter(is_active=True)

    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        if selected_items:
            try:
                # Get common data for all logs
                process_ids = request.POST.getlist('process')
                if not process_ids:
                    messages.error(request, 'Please select at least one process.')
                    return redirect('production_log_create')
                if len(process_ids) > 3:
                    messages.error(request, 'You can select up to 3 processes.')
                    return redirect('production_log_create')

                production_date = request.POST.get('production_date')
                facility_id = request.POST.get('facility')
                team_id = request.POST.get('team')

                # Create production logs for each selected item
                success_count = 0
                for item_id in selected_items:
                    try:
                        raw_data_item = RawData.objects.select_related('project').get(id=item_id)
                        quantity = request.POST.get(f'quantities[{item_id}]')

                        if quantity and quantity.strip():
                            # Create a production log for each selected process
                            for process_id in process_ids:
                                ProductionLog.objects.create(
                                    project_number=raw_data_item.project_number,
                                    log_designation=raw_data_item.log_designation,
                                    process_id=process_id,
                                    production_date=production_date,
                                    produced_quantity=float(quantity),
                                    facility_id=facility_id,
                                    team_id=team_id,
                                    created_by=request.user,
                                    status='completed'
                                )
                            success_count += 1

                    except RawData.DoesNotExist:
                        messages.error(request, f'Raw data item with ID {item_id} not found.')
                    except Exception as e:
                        messages.error(request, f'Error processing item {item_id}: {str(e)}')

                if success_count > 0:
                    messages.success(request, f'Successfully created {success_count} production log(s) for {len(process_ids)} process(es).')
                    return redirect('production_list')
            except Exception as e:
                messages.error(request, f'Error processing production logs: {str(e)}')
        else:
            messages.error(request, 'Please select at least one item to log.')

    context = {
        'log_items': log_items,
        'processes': processes,
        'facilities': facilities,
        'teams': teams,
        'title': 'Create Production Log',
    }

    return render(request, 'core/production_log_form.html', context)

@login_required
def quality_list(request):
    checks = QualityCheck.objects.select_related('production_log', 'inspector').order_by('-check_time')
    return render(request, 'core/quality_list.html', {'checks': checks})

@login_required
def quality_check_create(request, production_log_id):
    production_log = get_object_or_404(ProductionLog, id=production_log_id)
    
    if request.method == 'POST':
        form = QualityCheckForm(request.POST)
        if form.is_valid():
            quality_check = form.save(commit=False)
            quality_check.production_log = production_log
            quality_check.inspector = request.user
            quality_check.save()
            
            messages.success(request, 'Quality check added successfully.')
            return redirect('production_detail', pk=production_log.id)
    else:
        form = QualityCheckForm(initial={
            'production_log': production_log,
            'specification_min': 0,
            'specification_max': 0
        })
        # Hide the production_log field since we're setting it
        form.fields['production_log'].widget = forms.HiddenInput()
    
    context = {
        'form': form,
        'production_log': production_log,
        'title': 'Add Quality Check'
    }
    
    return render(request, 'core/quality_form.html', context)

@login_required
def material_usage_create(request, production_log_id):
    production_log = get_object_or_404(ProductionLog, pk=production_log_id)
    if request.method == 'POST':
        form = MaterialUsageForm(request.POST)
        if form.is_valid():
            usage = form.save(commit=False)
            usage.production_log = production_log
            
            # Update material stock
            material = usage.material
            material.quantity -= usage.quantity_used
            material.save()
            
            usage.save()
            messages.success(request, 'Material usage recorded successfully.')
            return redirect('production_detail', pk=production_log_id)
    else:
        form = MaterialUsageForm(initial={'production_log': production_log})
    return render(request, 'core/material_usage_form.html', {'form': form, 'title': 'Record Material Usage'})

@login_required
def material_detail(request, pk):
    material = get_object_or_404(Material, pk=pk)
    usage_history = MaterialUsage.objects.filter(material=material).order_by('-created_at')[:10]
    context = {
        'material': material,
        'usage_history': usage_history,
    }
    return render(request, 'core/material_detail.html', context)

@login_required
def production_detail(request, pk):
    production_log = get_object_or_404(ProductionLog, pk=pk)
    quality_checks = QualityCheck.objects.filter(production_log=production_log)
    material_usages = MaterialUsage.objects.filter(production_log=production_log)
    
    context = {
        'production_log': production_log,
        'quality_checks': quality_checks,
        'material_usages': material_usages,
    }
    return render(request, 'core/production_detail.html', context)

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    buildings = project.buildings.all()
    production_logs = ProductionLog.objects.filter(
        project_number=project.project_number
    ).order_by('-production_date')
    
    # Get previous and next projects
    previous_project = Project.objects.filter(pk__lt=pk).order_by('-pk').first()
    next_project = Project.objects.filter(pk__gt=pk).order_by('pk').first()
    
    # Calculate totals
    total_tonnage = buildings.aggregate(total=Sum('tonnage'))['total'] or 0
    total_area = buildings.aggregate(total=Sum('area'))['total'] or 0
    
    # Get production stats
    production_stats = project.get_production_stats()

    context = {
        'project': project,
        'buildings': buildings,
        'production_logs': production_logs,
        'total_tonnage': total_tonnage,
        'total_area': total_area,
        'production_stats': production_stats,
        'previous_project': previous_project,
        'next_project': next_project,
    }
    return render(request, 'core/project_detail.html', context)

@login_required
def process_list(request):
    processes = ProductionProcess.objects.all().order_by('category', 'name')
    return render(request, 'core/process_list.html', {'processes': processes})

@login_required
def process_detail(request, pk):
    process = get_object_or_404(ProductionProcess, pk=pk)
    logs = ProductionLog.objects.filter(process=process).order_by('-start_time')
    context = {
        'process': process,
        'logs': logs,
    }
    return render(request, 'core/process_detail.html', context)

@login_required
def process_create(request):
    if request.method == 'POST':
        form = ProductionProcessForm(request.POST)
        if form.is_valid():
            process = form.save()
            messages.success(request, 'Production process created successfully.')
            return redirect('process_detail', pk=process.pk)
    else:
        form = ProductionProcessForm()
    return render(request, 'core/process_form.html', {'form': form, 'title': 'Create Process'})

@login_required
def process_edit(request, pk):
    process = get_object_or_404(ProductionProcess, pk=pk)
    if request.method == 'POST':
        form = ProductionProcessForm(request.POST, instance=process)
        if form.is_valid():
            form.save()
            messages.success(request, 'Production process updated successfully.')
            return redirect('process_detail', pk=pk)
    else:
        form = ProductionProcessForm(instance=process)
    return render(request, 'core/process_form.html', {'form': form, 'title': 'Edit Process'})

@login_required
def raw_data_list(request):
    raw_data = RawData.objects.all().order_by('-created_at')

    # Apply filters if they exist in the request
    project_number = request.GET.get('project_number')
    log_designation = request.GET.get('log_designation')
    part_designation = request.GET.get('part_designation')
    assembly_mark = request.GET.get('assembly_mark')
    part_mark = request.GET.get('part_mark')

    if project_number:
        raw_data = raw_data.filter(project_number__icontains=project_number)
    if log_designation:
        raw_data = raw_data.filter(log_designation__icontains=log_designation)
    if part_designation:
        raw_data = raw_data.filter(part_designation__icontains=part_designation)
    if assembly_mark:
        raw_data = raw_data.filter(assembly_mark__icontains=assembly_mark)
    if part_mark:
        raw_data = raw_data.filter(part_mark__icontains=part_mark)

    return render(request, 'core/raw_data_list.html', {'raw_data': raw_data})

@login_required
def raw_data_detail(request, pk):
    raw_data = get_object_or_404(RawData, pk=pk)
    return render(request, 'core/raw_data_detail.html', {'raw_data': raw_data})

@login_required
def raw_data_create(request):
    if request.method == 'POST':
        form = RawDataForm(request.POST)
        if form.is_valid():
            raw_data = form.save()
            messages.success(request, 'Raw data entry created successfully.')
            return redirect('raw_data_detail', pk=raw_data.pk)
    else:
        form = RawDataForm()
    return render(request, 'core/raw_data_form.html', {'form': form, 'action': 'Create'})

@login_required
def raw_data_edit(request, pk):
    raw_data = get_object_or_404(RawData, pk=pk)
    if request.method == 'POST':
        form = RawDataForm(request.POST, instance=raw_data)
        if form.is_valid():
            raw_data = form.save()
            messages.success(request, 'Raw data entry updated successfully.')
            return redirect('raw_data_detail', pk=raw_data.pk)
    else:
        form = RawDataForm(instance=raw_data)
    return render(request, 'core/raw_data_form.html', {'form': form, 'action': 'Edit'})

@login_required
def raw_data_upload(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            excel_file = request.FILES['file']
            project_number = request.POST.get('project_number')
            
            if not project_number:
                messages.error(request, 'Please select a project')
                return redirect('raw_data_upload')
            
            # Read the Excel file
            df = pd.read_excel(excel_file)
            changes_made = False
            
            for index, row in df.iterrows():
                try:
                    # Extract data from row
                    log_designation = str(row.get('Log Designation', '')).strip()
                    part_designation = str(row.get('Part Designation', '')).strip()
                    assembly_mark = str(row.get('Assembly Mark', '')).strip()
                    part_mark = str(row.get('Part Mark', '')).strip()
                    name = str(row.get('Name', '')).strip()
                    quantity = float(row.get('Quantity', 0))
                    profile = str(row.get('Profile', '')).strip()
                    grade = str(row.get('Grade', '')).strip()
                    length = float(row.get('Length', 0))
                    net_area_single = float(row.get('Net Area Single', 0))
                    net_area_total = float(row.get('Net Area Total', 0))
                    single_part_weight = float(row.get('Single Part Weight', 0))
                    net_weight_total = float(row.get('Net Weight Total', 0))
                    new_revision = str(row.get('Revision', '')).strip()
                    building_designation = str(row.get('Building Designation', '')).strip()
                    building_name = str(row.get('Building Name', '')).strip()
                    
                    # Create raw data entry
                    raw_data = RawData.objects.create(
                        project_number=project_number,
                        building_designation=building_designation,
                        building_name=building_name,
                        log_designation=log_designation,
                        part_designation=part_designation,
                        assembly_mark=assembly_mark,
                        part_mark=part_mark,
                        name=name,
                        quantity=quantity,
                        profile=profile,
                        grade=grade,
                        length=length,
                        net_area_single=net_area_single,
                        net_area_total=net_area_total,
                        single_part_weight=single_part_weight,
                        net_weight_total=net_weight_total,
                        revision=new_revision
                    )
                    raw_data.save()
                    changes_made = True
                    
                except Exception as e:
                    messages.error(request, f'Error in row {index + 2}: {str(e)}')
                    return redirect('raw_data_upload')
            
            if changes_made:
                messages.success(request, 'Data uploaded successfully!')
            
            return redirect('raw_data_list')
            
        except Exception as e:
            messages.error(request, f'Error uploading file: {str(e)}')
            return redirect('raw_data_upload')
    
    # Get all projects for the dropdown
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'core/raw_data_upload.html', {'projects': projects})

@login_required
def get_filtered_log_designations(request):
    project_number = request.GET.get('project_number')
    part_type = request.GET.get('part_type')
    building_name = request.GET.get('building_name')
    search_term = request.GET.get('term', '').strip()
    
    # Start with all log designations
    queryset = RawData.objects.all()
    
    # Apply filters if they are provided and not empty
    if project_number and project_number != 'null':
        queryset = queryset.filter(project_number=project_number)
    
    if building_name and building_name != 'null':
        queryset = queryset.filter(building_name=building_name)
    
    if part_type and part_type != 'null':
        if part_type == 'assembly':
            queryset = queryset.filter(assembly_mark__isnull=False)
        elif part_type == 'single':
            queryset = queryset.filter(assembly_mark__isnull=True)
    
    # Apply search term if provided
    if search_term:
        queryset = queryset.filter(log_designation__icontains=search_term)
    
    # Get unique log designations
    log_designations = queryset.values_list('log_designation', flat=True).distinct()
    log_designations = sorted(set(ld for ld in log_designations if ld))
    
    # Format for Select2
    results = [{'id': ld, 'text': ld} for ld in log_designations]
    
    return JsonResponse({
        'results': results,
        'pagination': {'more': False}  # Add pagination info for Select2
    })

@login_required
def production_dashboard(request):
    # Get all projects that have raw data
    projects_with_data = Project.objects.filter(
        project_number__in=RawData.objects.values_list('project_number', flat=True).distinct()
    ).exclude(status='completed')
    
    # Get production statistics for each project
    project_stats = []
    for project in projects_with_data:
        # Get raw data quantities for this project
        raw_data_totals = RawData.objects.filter(
            project_number=project.project_number
        ).values('log_designation').annotate(
            total_quantity=Sum('quantity')
        )
        
        # Create a dictionary to store total quantities by log designation
        log_totals = {item['log_designation']: item['total_quantity'] for item in raw_data_totals}
        
        # Get production logs for this project's log designations
        production_logs = ProductionLog.objects.filter(
            project_number=project.project_number,
            log_designation__in=log_totals.keys()
        )
        
        # Calculate process-wise progress
        process_stats = {}
        processes = ProductionProcess.objects.filter(category='PRODUCTION')
        
        for process in processes:
            # Get produced quantity for this process
            produced_qty = production_logs.filter(
                process=process
            ).aggregate(
                total_produced=Sum('produced_quantity')
            )['total_produced'] or 0
            
            # Calculate total quantity from raw data
            total_qty = sum(log_totals.values())
            
            if total_qty > 0:
                percentage = (produced_qty / total_qty) * 100
            else:
                percentage = 0
                
            process_stats[process.name] = {
                'total_quantity': total_qty,
                'produced_quantity': produced_qty,
                'percentage': round(percentage, 1)
            }
        
        # Only include projects that have both raw data and production logs
        if any(stats['total_quantity'] > 0 for stats in process_stats.values()):
            project_stats.append({
                'project': project,
                'process_stats': process_stats
            })
    
    context = {
        'project_stats': project_stats,
        'title': 'Production Dashboard'
    }
    
    return render(request, 'core/production_dashboard.html', context)

@login_required
def building_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    buildings = project.buildings.all().order_by('building_number')
    
    context = {
        'project': project,
        'buildings': buildings,
        'title': f'Buildings - {project.name}'
    }
    return render(request, 'core/building_list.html', context)

@login_required
def building_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            building = form.save(commit=False)
            building.project = project
            building.save()
            messages.success(request, 'Building added successfully.')
            return redirect('building_list', project_id=project.id)
    else:
        form = BuildingForm()
    
    context = {
        'form': form,
        'project': project,
        'title': 'Add Building'
    }
    return render(request, 'core/building_form.html', context)

@login_required
def building_edit(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    
    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            form.save()
            messages.success(request, 'Building updated successfully.')
            return redirect('building_list', project_id=building.project.id)
    else:
        form = BuildingForm(instance=building)
    
    context = {
        'form': form,
        'building': building,
        'project': building.project,
        'title': 'Edit Building'
    }
    return render(request, 'core/building_form.html', context)

@login_required
def building_delete(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    project_id = building.project.id
    
    if request.method == 'POST':
        building.delete()
        messages.success(request, 'Building deleted successfully.')
        return redirect('building_list', project_id=project_id)
    
    context = {
        'building': building,
        'project': building.project,
        'title': 'Delete Building'
    }
    return render(request, 'core/building_delete.html', context)

@login_required
def production_log_edit(request, pk):
    production_log = get_object_or_404(ProductionLog, pk=pk)
    
    if request.method == 'POST':
        form = ProductionLogForm(request.POST, instance=production_log)
        if form.is_valid():
            form.save()
            messages.success(request, 'Production log updated successfully.')
            return redirect('production_list')
    else:
        form = ProductionLogForm(instance=production_log)
    
    context = {
        'form': form,
        'title': 'Edit Production Log',
        'production_log': production_log,
    }
    
    return render(request, 'core/production_log_form.html', context)

@login_required
def production_log_delete(request, pk):
    production_log = get_object_or_404(ProductionLog, pk=pk)
    
    if request.method == 'POST':
        # Store info for success message
        log_info = f"Production log for {production_log.log_designation} ({production_log.process.name})"
        
        # Delete the log
        production_log.delete()
        
        messages.success(request, f'{log_info} has been deleted.')
        return redirect('production_list')
    
    context = {
        'production_log': production_log,
        'title': 'Delete Production Log',
    }
    
    return render(request, 'core/production_log_delete.html', context)

@login_required
def production_log_bulk_delete(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_logs')
        if selected_ids:
            # Get the logs to delete
            logs_to_delete = ProductionLog.objects.filter(id__in=selected_ids)
            
            # Store count for success message
            deleted_count = logs_to_delete.count()
            
            # Delete the logs
            logs_to_delete.delete()
            
            messages.success(request, f'Successfully deleted {deleted_count} production logs.')
        else:
            messages.warning(request, 'No production logs were selected for deletion.')
            
    return redirect('production_list')

@login_required
def production_log_detail(request, pk):
    production_log = get_object_or_404(ProductionLog, pk=pk)
    quality_checks = production_log.qualitycheck_set.all().order_by('-check_time')
    material_usage = production_log.materialusage_set.all()
    
    # Get raw data information
    raw_data = RawData.objects.filter(
        project_number=production_log.project_number,
        log_designation=production_log.log_designation
    ).first()
    
    context = {
        'production_log': production_log,
        'quality_checks': quality_checks,
        'material_usage': material_usage,
        'raw_data': raw_data,
        'title': f'Production Log Detail - {production_log.log_designation}'
    }
    
    return render(request, 'core/production_log_detail.html', context)

@login_required
def get_buildings_by_project(request, project_id):
    buildings = Building.objects.filter(project_id=project_id).values('id', 'name')
    return JsonResponse(list(buildings), safe=False)
