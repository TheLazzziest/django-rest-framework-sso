import uuid
import six

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TokenMeta(models.Model):
    """
    The model for storing additional metadata the jwt token.
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text=_('a primary key of a model meta')
    )
    jti = models.TextField(
        editable=False,  verbose_name=_('a token jti claim value')
    )
    token = models.TextField(
        editable=False, verbose_name=_('a token representation')
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        abstract = (
            "rest_framework_sso" not in settings.INSTALLED_APPS and
            "rest_framework_simplejwt.token_blacklist" not in settings.INSTALLED_APPS
        )
        verbose_name = _("Session token")
        verbose_name_plural = _("Session tokens")
        indexes = [
            models.Index(fields=['ip_address']),
        ]

    def __str__(self):
        return six.text_type(self.token)
