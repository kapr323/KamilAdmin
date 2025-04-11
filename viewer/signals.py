from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee, JobPosition


# Přiřazení oprávnění k uživatelským účtům
def assign_permissions_to_user(user):
    # Implementace přiřazení oprávnění na základě role uživatele
    pass

# Signál pro vytvoření uživatele
@receiver(post_save, sender=User)
def assign_permissions_on_user_creation(sender, instance, created, **kwargs):
    if created:
        # Přiřazení oprávnění na základě role uživatele
        assign_permissions_to_user(instance)
