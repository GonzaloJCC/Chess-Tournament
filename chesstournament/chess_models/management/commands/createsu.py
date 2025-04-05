# catalog/management/commands/createsu.py

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        username = 'alumnodb'
        email = 'admin@myproject.com'
        password = 'alumnodb'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username,
                email,
                password
            )
        print('Superuser has been created.')