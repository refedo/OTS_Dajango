from django.core.management.base import BaseCommand
from core.models import Project, Building

class Command(BaseCommand):
    help = 'Creates sample projects and buildings'

    def handle(self, *args, **options):
        # Sample project numbers
        project_numbers = ['230', '236', '239', '241', '245']
        client_names = [
            'Saudi Aramco',
            'SABIC',
            'SEC',
            'Ma\'aden',
            'SWCC'
        ]
        
        for i, project_number in enumerate(project_numbers):
            # Create project
            project = Project.objects.create(
                project_number=project_number,
                name=f'Project {project_number}',
                client_name=client_names[i],
                status='in_progress'
            )
            self.stdout.write(self.style.SUCCESS(f'Created project: {project}'))

            # Create buildings for each project
            building_count = 3 if i < 2 else 2  # First two projects get 3 buildings, others get 2
            for j in range(building_count):
                building = Building.objects.create(
                    project=project,
                    name=f'Building {chr(65+j)}',  # Building A, B, C
                    description=f'Sample building {chr(65+j)} for project {project_number}'
                )
                self.stdout.write(self.style.SUCCESS(f'Created building: {building}'))
