from django.db import models
from users.models import CustomUser


class Follow(models.Model):
    followed_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followed')
    following_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
