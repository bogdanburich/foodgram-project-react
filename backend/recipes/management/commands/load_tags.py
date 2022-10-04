import os
from csv import DictReader

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand

from recipes.models import Tag

User = get_user_model()


class Command(BaseCommand):
    help = 'Load tags from csv file'

    def handle(self, *args, **options):

        file_path = os.path.join(settings.TEST_DATA_DIR, 'tags.csv')
        reader = DictReader(
            open(file_path, 'r', encoding='utf-8'),
        )
        for row in reader:
            try:

                tag = Tag(
                    name=row['name'],
                    color=row['color'],
                    slug=row['slug'],
                )
                tag.save()
                self.stdout.write(self.style.SUCCESS(f'Tag {tag} added'))

            except IntegrityError:
                self.stdout.write(self.style.ERROR(
                    f'Tag {tag} already loaded')
                )

        self.stdout.write(self.style.SUCCESS('Tags loaded successfully'))
