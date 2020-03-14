from django.conf.urls import url
from rest_framework_sso.viewsets import jwt as jwt_views

urlpatterns = [
    url(r"^jwt/create/?", jwt_views.SSObtainTokenView.as_view(), name="sso-jwt-create"),
    url(r"^jwt/refresh/?", jwt_views.SSORefreshTokenView.as_view(), name="sso-jwt-refresh"),
    url(r"^jwt/verify/?", jwt_views.SSOVerifyTokenView.as_view(), name="sso-jwt-verify"),
]