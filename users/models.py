from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class CustomUser(AbstractUser):
    followers = models.IntegerField(validators=[MinValueValidator(0)], default=0)
