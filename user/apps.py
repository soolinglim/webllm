from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField' # 'django.db.models.BigAutoField'
    name = 'user'
