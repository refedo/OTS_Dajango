from django.core.management.base import BaseCommand
from core.models import Project, Building

class Command(BaseCommand):
    help = 'Creates sample data for testing'

    def handle(self, *args, **options):
        # Create first project
        project1 = Project.objects.create(
            project_number='1001',
            name='Sample Project 1',
            client_name='ACME Corporation',
            status='in_progress'
        )
        self.stdout.write(self.style.SUCCESS(f'Created project: {project1}'))

        # Create buildings for first project
        for i in range(3):
            building = Building.objects.create(
                project=project1,
                name=f'Building {chr(65+i)}',  # Building A, B, C
                description=f'Sample building {chr(65+i)} for project {project1.project_number}'
            )
            self.stdout.write(self.style.SUCCESS(f'Created building: {building}'))

        # Create second project
        project2 = Project.objects.create(
            project_number='1002',
            name='Sample Project 2',
            client_name='TechCorp Inc.',
            status='not_started'
        )
        self.stdout.write(self.style.SUCCESS(f'Created project: {project2}'))

        # Create buildings for second project
        for i in range(2):
            building = Building.objects.create(
                project=project2,
                name=f'Building {chr(65+i)}',
                description=f'Sample building {chr(65+i)} for project {project2.project_number}'
            )
            self.stdout.write(self.style.SUCCESS(f'Created building: {building}'))
