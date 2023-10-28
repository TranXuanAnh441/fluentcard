from django.db import models
from django.conf import settings

# Create your models here.
class RoleplayPrompt(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )
    description = models.CharField(max_length=700)
    difficulty = models.IntegerField(default=1)
    image = models.URLField(max_length = 200, null=True)