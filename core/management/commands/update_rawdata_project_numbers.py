from django.core.management.base import BaseCommand
from core.models import RawData

class Command(BaseCommand):
    help = 'Updates project_number field for all existing RawData records'

    def handle(self, *args, **options):
        updated = 0
        for data in RawData.objects.filter(project_number=''):
            if data.project:
                data.project_number = data.project.project_number
                data.save()
                updated += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated} raw data records with project numbers'
            )
        )
