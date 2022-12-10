import factory
from django.apps import AppConfig
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# setup dependencies this factory relies on.
deps = []


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")
    password = make_password("fakepassword")
    email = factory.Sequence(lambda n: "person{}@example.com".format(n))
    is_active = True


def run(config: AppConfig, *args, **kwargs):
    # check if we have already run this factory and skip.
    if User.objects.all().count() > 0:
        return

    for _ in range(5):
        UserFactory()
