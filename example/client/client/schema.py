from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Schema configuration
schema_view = get_schema_view(
    openapi.Info(title="Django Rest Framework SSO: Client", default_version='dev'),
    validators=["flex", "ssv"],
    public=False,
    permission_classes=(permissions.AllowAny,),
)
