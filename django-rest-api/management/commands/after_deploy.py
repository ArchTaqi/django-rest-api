from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        call_command('migrate', interactive=False)
        call_command('loaddata', './DjangoRestApi/fixtures/initial_data.json')