from django.apps import AppConfig


# depends on account
deps = [
    "accounts",
]


def run(config: AppConfig, *args, **kwargs):
    print(config.name)
