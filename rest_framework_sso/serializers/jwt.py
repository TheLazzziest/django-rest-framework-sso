from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer
)

from rest_framework_sso.tokens import SSORefreshToken, SSOUntypedToken


class SSObtainTokenSerializer(TokenObtainPairSerializer):
    """
    An sso serializer for obtaining a jwt token
    """
    @classmethod
    def get_token(cls, user):
        return SSORefreshToken.for_user(user)


class SSORefreshTokenSerializer(TokenRefreshSerializer):
    pass


class SSOVerifyTokenSerializer(TokenVerifySerializer):

    def validate(self, attrs):
        SSOUntypedToken(attrs['token'])

        return {}