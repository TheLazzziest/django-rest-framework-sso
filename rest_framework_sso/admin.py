from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import TokenMeta


@admin.register(TokenMeta)
class TokenMetaModelAdmin(ModelAdmin):
    list_display = ('jti', 'created_at')
