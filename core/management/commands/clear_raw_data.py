from django.core.management.base import BaseCommand
from core.models import RawData

class Command(BaseCommand):
    help = 'Deletes all RawData entries from the database'

    def handle(self, *args, **options):
        count = RawData.objects.count()
        RawData.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} RawData entries')
        )
