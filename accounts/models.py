from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    must_change_password = models.BooleanField(default=True)    # Pole pro kontrolu, zda je potřeba změnit heslo

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # případně další pole

    def __str__(self):
        return f"{self.first_name} {self.ldb_old.sqlite3ast_name}"