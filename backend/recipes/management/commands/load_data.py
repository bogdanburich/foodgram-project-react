import os
from csv import DictReader

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag, Recipe

User = get_user_model()


class Command(BaseCommand):
    help = 'Load ingredients from csv file'

    def handle(self, *args, **options):

        try:
            # file_path = os.path.join(settings.TEST_DATA_DIR, 'ingredients.csv')
            # reader = DictReader(
            #     open(file_path, 'r', encoding='utf-8'),
            # )

            # for row in reader:
            #     ingredient = Ingredient(
            #         name=row['name'],
            #         measurement_unit=row['measurement_unit']
            #     )
            #     ingredient.save()
            #     self.stdout.write(self.style.SUCCESS(f'Ingredient {ingredient} added'))

            # self.stdout.write(self.style.SUCCESS('Ingredients loaded successfully'))

            # file_path = os.path.join(settings.TEST_DATA_DIR, 'users.csv')
            # reader = DictReader(
            #     open(file_path, 'r', encoding='utf-8'),
            # )

            # for row in reader:
            #     user = User.objects.create_user(
            #         email=row['email'],
            #         username=row['username'],
            #         first_name=row['first_name'],
            #         last_name=row['last_name'],
            #         password=row['password'],
            #     )
            #     self.stdout.write(self.style.SUCCESS(f'User {user} added'))

            # self.stdout.write(self.style.SUCCESS('Users loaded successfully'))

            # file_path = os.path.join(settings.TEST_DATA_DIR, 'tags.csv')
            # reader = DictReader(
            #     open(file_path, 'r', encoding='utf-8'),
            # )

            # for row in reader:
            #     tag = Tag(
            #         name=row['name'],
            #         color=row['color'],
            #         slug=row['slug'],
            #     )
            #     tag.save()
            #     self.stdout.write(self.style.SUCCESS(f'Tag {tag} added'))

            # self.stdout.write(self.style.SUCCESS('Tags loaded successfully'))

            file_path = os.path.join(settings.TEST_DATA_DIR, 'recipes.csv')
            reader = DictReader(
                open(file_path, 'r', encoding='utf-8'),
            )

            image = os.path.join(settings.TEST_DATA_DIR, 'image.png')

            for row in reader:
                recipe = Recipe(
                    name=row['name'],
                    image=image,
                    text=row['text'],
                    author=User.objects.get(pk=row['author_id']),
                    cooking_time=row['cooking_time'],
                )
                recipe.save()
                self.stdout.write(self.style.SUCCESS(f'Recipe {recipe} added'))

        except IntegrityError:
            self.stdout.write(self.style.ERROR('Data already loaded'))
