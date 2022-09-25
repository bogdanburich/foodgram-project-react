import os
from csv import DictReader

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

User = get_user_model()


class Command(BaseCommand):
    help = 'Load ingredients from csv file'

    def handle(self, *args, **options):

        self.stdout.write('Loading ingredients...')
        file_path = os.path.join(settings.TEST_DATA_DIR, 'ingredients.csv')
        reader = DictReader(
            open(file_path, 'r', encoding='utf-8'),
        )

        for row in reader:
            ingredient = Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )
            ingredient.save()
            self.stdout.write(self.style.SUCCESS(f'{ingredient} added!'))

        self.stdout.write(self.style.SUCCESS('Ingredients loaded successfully'))
