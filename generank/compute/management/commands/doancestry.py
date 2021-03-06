from django.core.management.base import BaseCommand, CommandError

from generank.compute import tasks


class Command(BaseCommand):
    help = 'Kicks off tasks to calculate the ancestry of a user.'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=str)

    def handle(self, *args, **options):
        user_id = options['user_id']

        tasks.cad.get_ancestry.delay(user_id)
        self.stdout.write(self.style.SUCCESS('Tasks dispatched'))
