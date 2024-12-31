from django.core.management.base import BaseCommand
from core.models import RawData, Project, Building
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Creates sample raw data for testing'

    def handle(self, *args, **kwargs):
        # Get existing projects
        projects = list(Project.objects.all())
        
        if not projects:
            self.stdout.write(self.style.ERROR('No projects found. Please create some projects first.'))
            return

        # Sample data
        log_designations = ['LOG-A', 'LOG-B', 'LOG-C']
        part_designations = ['PART-1', 'PART-2', 'PART-3']
        assembly_marks = ['ASM-X', 'ASM-Y', 'ASM-Z']
        part_marks = ['PM-01', 'PM-02', 'PM-03']
        profiles = ['IPE200', 'HEA300', 'UPN120']
        grades = ['S275JR', 'S355JR', 'S235JR']
        revisions = ['R0', 'R1', 'R2']

        # Create 10 sample records
        for i in range(10):
            project = random.choice(projects)
            # Get buildings for the selected project
            buildings = list(Building.objects.filter(project=project))
            building = random.choice(buildings) if buildings else None
            
            if not building:
                self.stdout.write(self.style.WARNING(f'No buildings found for project {project}. Skipping...'))
                continue

            RawData.objects.create(
                project=project,
                building=building,
                log_designation=random.choice(log_designations),
                part_designation=random.choice(part_designations),
                assembly_mark=random.choice(assembly_marks),
                part_mark=random.choice(part_marks),
                name=f'Sample Part {i+1}',
                quantity=random.randint(1, 10),
                profile=random.choice(profiles),
                grade=random.choice(grades),
                length=random.uniform(1000, 5000),
                net_area_single=random.uniform(0.5, 2.0),
                net_area_total=random.uniform(2.0, 10.0),
                single_part_weight=random.uniform(10, 100),
                net_weight_total=random.uniform(50, 500),
                revision=random.choice(revisions)
            )

        self.stdout.write(self.style.SUCCESS('Successfully created sample raw data'))
