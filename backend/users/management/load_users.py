import os
from csv import DictReader

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Load users from csv file'

    def handle(self, *args, **options):

        file_path = os.path.join(settings.TEST_DATA_DIR, 'users.csv')
        reader = DictReader(
            open(file_path, 'r', encoding='utf-8'),
        )

        for row in reader:

            try:
                user = User.objects.create_user(
                    email=row['email'],
                    username=row['username'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    password=row['password'],
                )
                self.stdout.write(self.style.SUCCESS(f'User {user} added'))

            except IntegrityError:
                self.stdout.write(self.style.ERROR('User already loaded'))

        self.stdout.write(self.style.SUCCESS('Users loaded successfully'))
