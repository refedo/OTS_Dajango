from django.core.management.base import BaseCommand
from core.models import ProductionLog

class Command(BaseCommand):
    help = 'Updates project_number field for all existing ProductionLog records'

    def handle(self, *args, **options):
        updated = 0
        for log in ProductionLog.objects.filter(project_number=''):
            if log.project:
                log.project_number = log.project.project_number
                log.save()
                updated += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated} production logs with project numbers'
            )
        )
