from django.apps import AppConfig
from .encryption import encryption_rsa


def key_set():
    encryption_rsa.create_key()


class SimplejwtAppConfig(AppConfig):
    key_set()
    default_auto_field = "django.db.models.BigAutoField"
    name = "SimpleJWT_app"
