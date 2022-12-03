from django.contrib.auth.models import User
from django.core.management import BaseCommand
from faker import Faker

_faker = Faker()


class Command(BaseCommand):
    help = "Create dummy users in the database"

    def handle(self, *args, **options):
        for _ in range(1, 5):
            User.objects.create_user(
                first_name=_faker.first_name(),
                last_name=_faker.last_name(),
                email=_faker.ascii_email(),
                password="fake_password",
                username=_faker.user_name(),
            )
