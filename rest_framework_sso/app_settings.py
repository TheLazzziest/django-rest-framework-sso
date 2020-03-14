# coding: utf-8
from __future__ import absolute_import, unicode_literals

import datetime

from django.conf import settings
from django.test.signals import setting_changed

from rest_framework.settings import APISettings

from .utils import ObjDict


USER_SETTINGS = getattr(settings, "REST_FRAMEWORK_SSO", None)

DEFAULTS = {

    "ACCESS_TOKEN_CLASSES": settings.SIMPLE_JWT.get('ACCESS_TOKEN', ('rest_framework_sso.tokens.SSOAccessToken',)),

    "SSO_SERIALIZERS": ObjDict({
        'obtain_token': 'rest_framework_sso.serializers.jwt.SSObtainTokenSerializer',
        'refresh_token': 'rest_framework_sso.serializers.jwt.SSORefreshTokenSerializer',
        'verify_token': 'rest_framework_sso.serializers.jwt.SSOVerifyTokenSerializer'
    }),

    # site-cookie(session) token (http-only)
    # https://github.com/SimpleJWT/django-rest-framework-simplejwt/pull/157

    # Required configurations for an any server
    "SUBJECT": settings.SIMPLE_JWT.get('SUBJECT', None),  # https://tools.ietf.org/html/rfc7519#section-4.1.2
    "ISSUER": settings.SIMPLE_JWT.get('ISSUER', None),  # https://tools.ietf.org/html/rfc7519#section-4.1.1

    # Required for the identity server
    "EXPIRATION": settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME", datetime.timedelta(seconds=600)),  # https://tools.ietf.org/html/rfc7519#section-4.1.4
    "AUDIENCE": settings.SIMPLE_JWT.get("AUDIENCE"),  # https://tools.ietf.org/html/rfc7519#section-4.1.3
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = ()

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):
    global api_settings
    setting, value = kwargs["setting"], kwargs["value"]
    if setting == "REST_FRAMEWORK_SSO":
        api_settings = APISettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_api_settings)
