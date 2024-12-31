import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ots_django.settings')
django.setup()

from core.models import Project, Building

def create_sample_data():
    # Create a new project
    project = Project.objects.create(
        project_number='1001',
        name='Sample Project 1',
        client_name='ACME Corporation',
        status='in_progress'
    )
    print(f"Created project: {project}")

    # Create buildings for the project
    buildings = [
        Building.objects.create(
            project=project,
            name=f'Building {chr(65+i)}',  # Building A, B, C
            description=f'Sample building {chr(65+i)} for project {project.project_number}'
        )
        for i in range(3)
    ]
    
    for building in buildings:
        print(f"Created building: {building}")

    # Create another project
    project2 = Project.objects.create(
        project_number='1002',
        name='Sample Project 2',
        client_name='TechCorp Inc.',
        status='not_started'
    )
    print(f"Created project: {project2}")

    # Create buildings for the second project
    buildings2 = [
        Building.objects.create(
            project=project2,
            name=f'Building {chr(65+i)}',
            description=f'Sample building {chr(65+i)} for project {project2.project_number}'
        )
        for i in range(2)
    ]
    
    for building in buildings2:
        print(f"Created building: {building}")

if __name__ == '__main__':
    create_sample_data()
