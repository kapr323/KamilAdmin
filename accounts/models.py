from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Použití emailu jako login:
    email = models.EmailField(unique=True)
    # Přidání příznaku, že uživatel musí změnit heslo při prvním přihlášení
    must_change_password = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"