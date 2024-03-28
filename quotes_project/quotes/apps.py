from django.apps import AppConfig


class QuotesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "quotes"

    def ready(self):
        from .scheduler.runapscheduler import Command

        run_command = Command()
        run_command.handle()
