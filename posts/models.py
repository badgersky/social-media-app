from django.core.validators import MinValueValidator
from django.db import models
from users.models import CustomUser


class Tweet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
