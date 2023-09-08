from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Programmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
