from django.apps import AppConfig


class HelloConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hello'
    verbose_name = 'An Application for Cookies Testing'
