from django.core.management.base import BaseCommand
from core.models import Project, Building
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Creates sample projects and buildings'

    def handle(self, *args, **options):
        # Sample project data
        projects_data = [
            {
                'estimation_number': 'EST-230',
                'project_number': '230',
                'name': 'Industrial Complex A',
                'project_manager': 'Ahmed Ali',
                'client_name': 'Saudi Aramco',
                'contract_date': date(2024, 1, 15),
                'structure_type': 'INDUSTRIAL',
                'number_of_structures': 3,
                'incoterm': 'EXW',
                'scope_of_work': 'Construction of industrial facility including warehouses and offices',
                'project_nature': 'NEW',
                'contractual_tonnage': 1500.00,
                'engineering_tonnage': 1550.00,
                'galvanized': True,
                'galvanization_microns': 85,
                'area': 12000.00,
                'm2_per_ton': 8.00,
                'welding_process': 'GMAW',
                'welding_wire_aws_class': 'ER70S-6',
                'pqr_no': 'PQR-2024-001',
                'wps_no': 'WPS-2024-001',
                'standard_code': 'AWS D1.1'
            },
            {
                'estimation_number': 'EST-236',
                'project_number': '236',
                'name': 'Commercial Center B',
                'project_manager': 'Mohammed Hassan',
                'client_name': 'SABIC',
                'contract_date': date(2024, 2, 1),
                'structure_type': 'COMMERCIAL',
                'number_of_structures': 2,
                'incoterm': 'FOB',
                'scope_of_work': 'Construction of commercial center with retail spaces',
                'project_nature': 'NEW',
                'contractual_tonnage': 800.00,
                'engineering_tonnage': 820.00,
                'galvanized': False,
                'area': 6000.00,
                'm2_per_ton': 7.50,
                'welding_process': 'FCAW',
                'welding_wire_aws_class': 'E71T-1',
                'pqr_no': 'PQR-2024-002',
                'wps_no': 'WPS-2024-002',
                'standard_code': 'AWS D1.1'
            },
            {
                'estimation_number': 'EST-239',
                'project_number': '239',
                'name': 'Warehouse Complex C',
                'project_manager': 'Khalid Omar',
                'client_name': 'SEC',
                'contract_date': date(2024, 2, 15),
                'structure_type': 'WAREHOUSE',
                'number_of_structures': 4,
                'incoterm': 'CIF',
                'scope_of_work': 'Construction of warehouse complex with loading bays',
                'project_nature': 'NEW',
                'contractual_tonnage': 2000.00,
                'engineering_tonnage': 2100.00,
                'galvanized': True,
                'galvanization_microns': 90,
                'area': 15000.00,
                'm2_per_ton': 7.50,
                'welding_process': 'SMAW',
                'welding_wire_aws_class': 'E7018',
                'pqr_no': 'PQR-2024-003',
                'wps_no': 'WPS-2024-003',
                'standard_code': 'AWS D1.1'
            }
        ]

        for project_data in projects_data:
            # Create project
            project = Project.objects.create(**project_data)
            self.stdout.write(self.style.SUCCESS(f'Created project: {project}'))

            # Create buildings for each project
            building_count = project_data['number_of_structures']
            for j in range(building_count):
                building = Building.objects.create(
                    project=project,
                    name=f'Building {chr(65+j)}',  # Building A, B, C, etc.
                    description=f'Sample building {chr(65+j)} for project {project_data["project_number"]}'
                )
                self.stdout.write(self.style.SUCCESS(f'Created building: {building}'))
