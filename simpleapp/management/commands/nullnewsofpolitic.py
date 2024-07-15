from django.core.management.base import BaseCommand, CommandError
from simpleapp.models import Post


class Command(BaseCommand):
    help = 'Подсказка вашей команды'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all news about sport? yes/no')
        answer = input()

        if answer == 'yes':
            Post.objects.filter(postCategory=2, category_type='NW').delete()
            self.stdout.write(self.style.SUCCESS('Succesfully wiped news about sport!'))
            return

        self.stdout.write(
            self.style.ERROR('Access denied'))
