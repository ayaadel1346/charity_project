from django.core.management.base import BaseCommand
from django.utils import timezone
from project.models import ActivationLink

class Command(BaseCommand):
    help = 'Expires activation links older than 24 hours'

    def handle(self, *args, **kwargs):
        threshold = timezone.now() - timezone.timedelta(hours=24)
        expired_links = ActivationLink.objects.filter(created_at__lt=threshold)
        expired_links.delete()
