import os
import logging
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

# Set up logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create a superuser.'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        # Check if the environment variables are set
        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR('Environment variables for superuser creation are not set properly.'))
            return

        try:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully.'))
            else:
                self.stdout.write(self.style.WARNING(f'Superuser {username} already exists. Skipping creation.'))
        except IntegrityError as e:
            self.stdout.write(self.style.WARNING(f'IntegrityError: {e}'))
            logger.error(f'IntegrityError when creating superuser {username}: {e}')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'An unexpected error occurred: {e}'))
            logger.error(f'Unexpected error when creating superuser {username}: {e}')
