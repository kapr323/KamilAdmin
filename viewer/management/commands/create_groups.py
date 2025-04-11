from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from viewer.models import Employee


class Command(BaseCommand):
    help = 'Vytvoří základní uživatelské skupiny a přístupová práva podle job_position'

    def handle(self, *args, **kwargs):
        # Vytvoření skupiny Admin
        admin_group, created = Group.objects.get_or_create(name='Admin')

        # Vytvoření rolí na základě job_position v Employee modelu
        positions = ['Tajemník', 'Starosta', 'Developer', 'Employee']

        for position in positions:
            # Vytvoření skupiny pro každou job_position
            group, created = Group.objects.get_or_create(name=position)

            # Pokud pozice je 'Manager', přidáme k této roli širší přístup
            if position == 'Tajemník':
                employee_permissions = Permission.objects.filter(
                    content_type=ContentType.objects.get_for_model(Employee))
            else:
                # Základní oprávnění pro zaměstnance (např. čtení a úprava svého profilu)
                employee_permissions = Permission.objects.filter(
                    content_type=ContentType.objects.get_for_model(Employee)).exclude(codename='change_employee')

            # Nastavení práv pro každou roli
            group.permissions.set(employee_permissions)

        self.stdout.write(self.style.SUCCESS('Skupiny a práva podle job_position byly úspěšně vytvořeny!'))
