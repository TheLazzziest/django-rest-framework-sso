from django.db import models


class Profile(models.Model):

    email = models.EmailField(primary_key=True, verbose_name="a user profile")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        indexes = [
            models.Index(fields=['email',])
        ]