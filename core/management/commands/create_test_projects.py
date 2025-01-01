from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from core.models import Project, Building

class Command(BaseCommand):
    help = 'Creates 5 test projects with sample data'

    def handle(self, *args, **kwargs):
        # Sample data for projects
        project_names = [
            "Industrial Warehouse Complex",
            "Commercial Office Building",
            "Airport Terminal Extension",
            "Sports Complex",
            "Shopping Mall Development"
        ]
        
        project_managers = [
            "John Smith",
            "Sarah Johnson",
            "Michael Chen",
            "Emily Brown",
            "David Wilson"
        ]
        
        clients = [
            "Global Industries Ltd",
            "Metro Development Corp",
            "National Airports Authority",
            "City Sports Department",
            "Retail Ventures Inc"
        ]
        
        structure_types = [
            ('industrial', 'Industrial Building'),
            ('commercial', 'Commercial Building'),
            ('infrastructure', 'Infrastructure'),
            ('commercial', 'Commercial Building'),
            ('commercial', 'Commercial Building')
        ]
        
        project_natures = [
            'new',
            'renovation',
            'expansion',
            'new',
            'new'
        ]
        
        erection_subcontractors = [
            "Elite Construction Co.",
            "Urban Builders LLC",
            "Aviation Construction Specialists",
            "Sports Facility Builders",
            "Mega Construction Group"
        ]

        # Create 5 test projects
        for i in range(5):
            # Calculate dates
            base_date = timezone.now()
            contract_date = base_date - timedelta(days=random.randint(15, 45))
            
            # Create project
            project = Project.objects.create(
                estimation_number=f'EST-2024-{i+1:03d}',
                project_number=f'PRJ-2024-{i+1:03d}',
                name=project_names[i],
                project_manager=project_managers[i],
                client_name=clients[i],
                status='in_progress',
                structure_type=structure_types[i][0],
                number_of_structures=random.randint(1, 5),
                project_nature=project_natures[i],
                erection_subcontractor=erection_subcontractors[i],
                contract_date=contract_date,
                down_payment=random.choice([20.00, 25.00, 30.00]),
                down_payment_ack=random.choice([True, False]),
                preliminary_retention=random.choice([10.00, 12.00, 15.00]),
                ho_retention=random.choice([5.00, 8.00, 10.00]),
                incoterm=random.choice(['EXW', 'FOB', 'CIF', 'DDP']),
                scope_of_work=f"Complete {structure_types[i][1].lower()} project including structural steel work and finishing",
                contractual_tonnage=random.randint(500, 2000),
                engineering_tonnage=random.randint(500, 2000),
                m2_per_ton=random.uniform(8.0, 12.0),
                galvanized=random.choice([True, False]),
                galvanization_microns=random.choice([80, 85, 90, 95, 100]) if random.choice([True, False]) else None,
                paint_coat_1=random.choice(['Epoxy Primer', 'Zinc Rich Primer', 'Alkyd Primer']),
                paint_coat_2=random.choice(['Epoxy Intermediate', 'Polyurethane', 'High Build Epoxy']),
                paint_coat_3=random.choice(['Polyurethane Topcoat', 'Acrylic Topcoat', None]),
                paint_coat_4=None,
                coat_1_microns=random.choice([60, 75, 80]),
                coat_2_microns=random.choice([120, 150, 180]),
                coat_3_microns=random.choice([50, 60, 70]) if random.choice(['Polyurethane Topcoat', 'Acrylic Topcoat']) else None,
                coat_4_microns=None,
                welding_process=random.choice(['GMAW', 'FCAW', 'SAW']),
                welding_wire_aws_class=random.choice(['ER70S-6', 'E71T-1', 'F7A2-EM12K']),
                wps_no=f'WPS-{random.randint(100, 999)}',
                pqr_no=f'PQR-{random.randint(100, 999)}',
                standard_code=random.choice(['AWS D1.1', 'EN 1090-2', 'AISC 360'])
            )
            
            # Create buildings for each project
            num_buildings = random.randint(1, 3)
            for j in range(num_buildings):
                Building.objects.create(
                    project=project,
                    name=f'Building {chr(65+j)}',  # Building A, B, C, etc.
                    description=f'Main structure for {project_names[i]} - Building {chr(65+j)}',
                    status='in_progress',
                    progress=random.randint(0, 100),
                    design_start_date=contract_date + timedelta(days=random.randint(15, 30)),
                    design_end_date=contract_date + timedelta(days=random.randint(45, 60)),
                    shop_drawing_start_date=contract_date + timedelta(days=random.randint(30, 45)),
                    shop_drawing_end_date=contract_date + timedelta(days=random.randint(60, 75)),
                    planned_start_date=contract_date + timedelta(days=random.randint(45, 60)),
                    planned_end_date=contract_date + timedelta(days=random.randint(180, 240)),
                    tonnage=random.randint(100, 500),
                    area=random.randint(500, 2000)
                )
            
            self.stdout.write(self.style.SUCCESS(f'Successfully created project "{project.name}" with {num_buildings} buildings'))
