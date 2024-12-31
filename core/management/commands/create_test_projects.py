from django.core.management.base import BaseCommand
from core.models import Project
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Creates 5 test projects with sample data'

    def handle(self, *args, **kwargs):
        # Sample data for projects
        project_types = ['Industrial', 'Commercial', 'Residential', 'Infrastructure']
        structure_types = ['Steel Structure', 'Mixed Structure', 'Heavy Structure']
        project_natures = ['New Construction', 'Renovation', 'Extension']
        incoterms = ['EXW', 'FOB', 'CIF', 'DDP']
        paint_systems = ['System A', 'System B', 'System C']
        welding_processes = ['GMAW', 'FCAW', 'SMAW']
        statuses = ['Active', 'On Hold', 'Completed', 'Planning']

        # Create 5 test projects
        for i in range(1, 6):
            # Calculate dates
            base_date = timezone.now()
            contract_date = base_date - timedelta(days=random.randint(30, 90))
            planned_start = contract_date + timedelta(days=random.randint(15, 45))
            planned_end = planned_start + timedelta(days=random.randint(90, 180))
            
            # Random boolean for is_galvanized
            is_galvanized = random.choice([True, False])
            
            project = Project.objects.create(
                estimation_number=f'EST-2024-{i:03d}',
                project_number=f'PRJ-2024-{i:03d}',
                project_name=f'Test Project {i}',
                project_manager=f'Manager {i}',
                client_name=f'Client Company {i}',
                status=random.choice(statuses),
                structure_type=random.choice(structure_types),
                number_of_structures=random.randint(1, 5),
                project_nature=random.choice(project_natures),
                erection_sub=f'Erection Company {i}',
                contract_date=contract_date,
                planned_start_date=planned_start,
                planned_end_date=planned_end,
                down_payment=random.randint(10, 30),
                down_payment_received=random.choice([True, False]),
                preliminary_retention=random.randint(5, 15),
                ho_retention=random.randint(5, 10),
                incoterm=random.choice(incoterms),
                scope_of_work=f'Detailed scope of work for Test Project {i}',
                contractual_tonnage=random.randint(100, 1000),
                engineering_tonnage=random.randint(100, 1000),
                area=random.randint(1000, 5000),
                m2_per_ton=random.uniform(10.0, 20.0),
                is_galvanized=is_galvanized,
                galvanization_microns=random.randint(50, 100) if is_galvanized else None,
                paint_system=random.choice(paint_systems),
                welding_process=random.choice(welding_processes),
                welding_wire=f'Wire Type {random.randint(1, 3)}',
                pqr_wps_number=f'PQR-{random.randint(100, 999)}',
                standard_code=f'STD-{random.randint(1000, 9999)}'
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created project "{project.project_name}"')
            )
