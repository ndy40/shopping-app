import importlib

from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand


executed_factories = []


def _run_factories(config, mod, *args, **options):
    if config.name in executed_factories:
        return

    print(f"Executing factories for {config.name}")
    run_func = getattr(mod, "run")
    run_func(config, *args, **options)
    executed_factories.append(config.name)


def _run_deps(deps: list):
    for dep in deps:
        app_config = apps.get_app_config(dep)
        module = importlib.import_module(
            ".seed_factories", app_config.module.__package__
        )
        _run_factories(app_config, module)


class Command(BaseCommand):
    help = "Run database seeder for each app. Each app needs to have a `seed_factory.py` file."

    def handle(self, *args, **options):
        for config in apps.get_app_configs():
            if config.name in settings.LOCAL_APPS:
                try:
                    module = importlib.import_module(
                        ".seed_factories", config.module.__package__
                    )

                    # TODO: handle dependencies
                    deps = getattr(module, "deps", [])

                    if deps:
                        _run_deps(deps)

                    if not hasattr(module, "run"):
                        continue

                    _run_factories(config, module, args, options)
                except ModuleNotFoundError:
                    pass
