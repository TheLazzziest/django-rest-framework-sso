from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, BlacklistMixin, UntypedToken
from rest_framework_simplejwt.utils import format_lazy
from django.utils.translation import ugettext_lazy as _

from .models import TokenMeta
from .app_settings import api_settings
from .claims import (
    ISSUER, AUDIENCE,
)


class SSOBlacklistMixin(BlacklistMixin):
    """
    If the `rest_framework_simplejwt.token_blacklist` app was configured to be
    used, tokens created from `BlacklistMixin` subclasses will insert
    themselves into an outstanding token list and also check for their
    membership in a token blacklist.
    """
    if 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
        @classmethod
        def for_user(cls, user):
            """
            Adds this token to the outstanding token list.
            """

            token = super().for_user(user)

            TokenMeta.objects.get_or_create(
                jti=token['jti'],
                token=str(token),
            )

            return token


class SSOSessionToken(AccessToken):
    pass


class SSOAccessToken(AccessToken):
    """
    SSO access token with additional claims:
    """

    def set_issuer(self, claim=ISSUER):
        """
        Set the issuer server of the payload
        :param claim:
        :return:
        """
        if api_settings.ISSUER is not None:
            self.payload[claim] = api_settings.ISSUER

    def check_issuer(self, claim=ISSUER):
        if claim not in self.payload:
            raise TokenError(format_lazy(_("Token has no '{}' claim"), claim))

        if self.payload[claim] != api_settings.ISSUER:
            raise TokenError(_('Token has wrong issuer'))

    def set_audience(self, claim=AUDIENCE):
        """
        Set the token audience for validation
        :param claim:
        :return:
        """
        if api_settings.AUDIENCE is not None:
            self.payload[claim] = api_settings.AUDIENCE

    def check_audience(self, claim=AUDIENCE):

        if claim not in self.payload:
            raise TokenError(format_lazy(_("Token has no '{}' claim"), claim))

        if self.payload[claim] != api_settings.AUDIENCE:
            raise TokenError(_('Token has wrong audience'))


class SSORefreshToken(SSOBlacklistMixin, RefreshToken):

    @property
    def access_token(self):
        """
        Returns an access token created from this refresh token.  Copies all
        claims present in this refresh token to the new access token except
        those claims listed in the `no_copy_claims` attribute.
        """
        access = import_string(api_settings.ACCESS_TOKEN_CLASS)()

        # Use instantiation time of refresh token as relative timestamp for
        # access token "exp" claim.  This ensures that both a refresh and
        # access token expire relative to the same time if they are created as
        # a pair.
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        access.set_issuer()
        access.set_audience()

        # in order to encode token with new claims
        return str(access)


class SSOUntypedToken(UntypedToken):
    pass
