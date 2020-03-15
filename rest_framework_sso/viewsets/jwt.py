# coding: utf-8

from rest_framework_sso.app_settings import api_settings as settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


from .mixins import MetaExtractorMixin


class SSObtainTokenView(MetaExtractorMixin, TokenObtainPairView):
    serializer_class = settings.SSO_SERIALIZERS.obtain_token


class SSORefreshTokenView(TokenRefreshView):
    serializer_class = settings.SSO_SERIALIZERS.refresh_token


class SSOVerifyTokenView(TokenVerifyView):
    serializer_class = settings.SSO_SERIALIZERS.verify_token