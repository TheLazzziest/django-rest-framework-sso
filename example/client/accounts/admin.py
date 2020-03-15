from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
