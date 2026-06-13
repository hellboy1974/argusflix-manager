from django.apps import AppConfig

class AppBuilderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.appbuilder'
    verbose_name = 'App Builder'

    def ready(self):
        import apps.appbuilder.signals
