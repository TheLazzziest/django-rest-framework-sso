from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RestFrameworkSSOConfig(AppConfig):
    name = "rest_framework_sso"
    verbose_name = _('Rest Framework SSO')
