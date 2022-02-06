from django.apps import AppConfig


class SaleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sale'
    verbose_name = 'Ventas | Facturas'

    def ready(self):
        # post_save.connect(save_hash, sender=User)
        import sale.signals
