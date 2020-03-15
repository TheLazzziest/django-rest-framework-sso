=========================
Django REST Framework SSO
=========================

Django REST Framework SSO is an extension built upon DRF_ and SimpleJWT_ that enables
Single sign-on in a microservice-oriented environment using the JWT standard.

.. _DRF: https://www.django-rest-framework.org/
.. _SimpleJWT: https://github.com/SimpleJWT/django-rest-framework-simplejwt


This library provides two types of JWT tokens:

1. non-expiring session tokens for your primary login application (aka. "refresh tokens")

2. short-lived authorization tokens for accessing your other apps (these contain permissions given by the primary app)

The client is expected to first login to your primary login application by POSTing an username and password.
The client will receive a refresh token and access token that will allow subsequent requests to the same server and other server which are connected to it.

Quick start
-----------

1. Add "rest_framework_sso" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework_simplejwt',
        'rest_framework_sso',
    ]

2. Include the session and authorization token URLs::

    urlpatterns = [
        ...
        url(r'^sso/', include("rest_framework_sso.urls.jwt"))
    ]

3. Override acces token class in SimpleJWT settings::

    SIMPLE_JWT = {
        ...
        'AUTH_TOKEN_CLASSES': ('rest_framework_sso.tokens.SSOAccessToken',),
    }

4. Add authentications::

    'DEFAULT_AUTHENTICATION_CLASSES': [
        "rest_framework_sso.authentication.SSOJWTTokenUserAuthentication",
        "rest_framework_sso.authentication.SSOSessionAuthentication",
        ....
    ]

5. Generate ssl keys for verifying/signing a jwt payload

Additional data in authorization tokens
---------------------------------------
For example, you may want to include an `account` field in your JWT authorization tokens,
so that `otherapp` will know about the user's permissions. To do this, you may need to override
the ObtainAuthorizationTokenView and AuthorizationTokenSerializer::

    class ExampleObtainTokenSerializer(rest_framework_sso.serializers.jwt.SSObtainTokenSerializer):
        """
        Returns a JSON Web Token that can be used for authenticated requests.
        """


JWT Authentication
------------------
In order to configuring jwt token, use SimpleJWT settings_.

.. _settings: https://github.com/SimpleJWT/django-rest-framework-simplejwt#settings

If you want to add custom claims, just override SSORefreshToken model and
write your custom JWT payload fields::

    from rest_framework_sso.tokens import SSOAccessToken

    class CustomSSOAccessToken(SSOAccessToken):
        def custom_claim(self, claim='new_claim'):
            self.payload[claim] = 'new_claim_value'


Add it to SimpleJWT settings doing the following::

    SIMPLE_JWT = {
        'ACCESS_TOKEN_CLASSES': ('otherapp.tokens.CustomSSOAccessToken',),
        ...
    }

Enable JWT authentication in the REST_FRAMEWORK settings::

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_sso.authentication.JWTAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            ...
        ),
        ...
    }

Requests that have been successfully authenticated with JWTAuthentication contain
the JWT payload data in the `request.auth` variable. This data can be used in your
API views/viewsets to handle permissions, for example::

    from rest_framework_sso import claims
    
    class UserViewSet(viewsets.ReadOnlyModelViewSet):
        serializer_class = UserSerializer
        queryset = User.objects.none()

        def get_queryset(self):
            if not request.user.is_authenticated or not request.auth:
                return self.none()
            return User.objects.filter(
                service=request.auth.get(claims.ISSUER),
                external_id=request.auth.get(claims.USER_ID),
            )

Settings
--------
The app settings must be placed inside REST_FRAMEWORK_SSO

SSO_SERIALIZERS
    A set of token serializers for handling token-related manipulations::

    * obtain_token - a serializer for crafting a new token
    * refresh_token - a serializer for renewing an already crafted token
    * verify_token - a serializer for verifying a token

ACCESS_TOKEN_CLASS
    A dot path to token class for processing access token

Samples
-------
Settings for the app that signing tokens for any client app::

    SIMPLE_JWT = {
        'ISSUER': 'authority',
        'SUBJECT': 'authority',
        'AUDIENCE': ['client', ...],
        'ALGORITHM': 'RSA256',
        'VERIFYING_KEY': '<private key string>'
    }

Example settings for project that accepts tokens signed by `authority` private key for `client`::

    SIMPLE_JWT = {
        'ISSUER': 'authority',
        'SUBJECT': 'client',
        'ALGORITHM': 'RSA256',
        'VERIFYING_KEY': '<public key string>'
    }



Generating RSA keys
-------------------
See the gist_.

.. _gist: https://gist.github.com/ygotthilf/baa58da5c3dd1f69fae9


