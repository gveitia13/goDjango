from django.apps import AppConfig


class ApkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apk'
    verbose_name = 'Configuraciones'

    def ready(self):
        # post_save.connect(save_hash, sender=User)
        import apk.signals
