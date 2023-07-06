from django.db import models
from django.contrib.auth.models import User

class UserCreation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username