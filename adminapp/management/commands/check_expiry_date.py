from django.core.management.base import BaseCommand
from django.utils import timezone
from adminapp.models import AccessKey

class Command(BaseCommand):
    help = 'Updates expired access keys'

    def handle(self, *args, **options):
        today = timezone.now().date()
        expired_keys = AccessKey.objects.filter(status='active', expiry_date__lt=today)

        for key in expired_keys:
            key.status = 'expired'
            key.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {len(expired_keys)} expired access keys.'))
