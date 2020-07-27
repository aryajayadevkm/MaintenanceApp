from django.apps import AppConfig


class JwtauthAppConfig(AppConfig):
    name = 'jwtauth'
    label = 'jwtauth'
    verbose_name = 'jwtauth'

    def ready(self):
        from jwtauth import signals

# This is how we register our custom app config with Django. Django is smart
# enough to look for the `default_app_config` property of each registered app
# and use the correct app config based on that value.


default_app_config = 'jwtauth.JwtauthAppConfig'
