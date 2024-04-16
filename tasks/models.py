from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from rest_framework.response import Response


class User(AbstractUser):
    pass


class Task(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
