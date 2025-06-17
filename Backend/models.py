from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    role = models.CharField(max_length=30)
    description = models.CharField(max_length=500)


class Membre(AbstractUser):
    photo = models.ImageField(upload_to="authentication")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Membre"
