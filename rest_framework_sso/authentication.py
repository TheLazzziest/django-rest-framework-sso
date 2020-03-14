from rest_framework import authentication as drf_auth
from rest_framework_simplejwt import authentication as simplejwt_auth


class SSOSessionAuthentication(drf_auth.SessionAuthentication):

    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged in user.
        Otherwise returns `None`.
        """

        # Get the session-based user from the underlying HttpRequest object
        user = getattr(request._request, 'user', None)

        # Unauthenticated, CSRF validation not required
        if not user or not user.is_active:
            return None

        self.enforce_csrf(request)

        # CSRF passed with authenticated user
        return (user, None)


class SSOJWTTokenUserAuthentication(simplejwt_auth.JWTTokenUserAuthentication):
    """
    JWT token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "JWT ".  For example:

    Authorization: JWT eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJsb2NhbG...
    """

    def authenticate(self, request):
        credentials = super().authenticate(request)
        if credentials is None:
            return None
        user, token = credentials
        return user, token
