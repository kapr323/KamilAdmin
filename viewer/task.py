from celery import shared_task
from django.core.mail import send_mail
from datetime import date

from viewer.models import Employee


@shared_task
def send_work_anniversary_email():
    """
    Posílá e-maily zaměstnancům k pracovnímu výročí.
    """
    today = date.today()
    employees = Employee.objects.filter(start_date_of_employment__month=today.month, start_date_of_employment__day=today.day)

    for employee in employees:
        send_mail(
            subject="Gratulace k pracovnímu výročí! 🎉",
            message=f"Dobrý den {employee.name},\n\nDnes slavíte {today.year - employee.start_date_of_employment.year}. pracovní výročí, srdečně gratuluji! 🎉",
            from_email="kamil.dvorak@email.cz",
            recipient_list=[employee.email],
            fail_silently=False,
        )

    return f"Emails sent to {len(employees)} employees"


@shared_task
def send_test_email():
    send_mail(
        'Testovací e-mail',
        'Tento e-mail je testovací zprávou.',
        'kamil.dvorak@email.cz',
        ['kamil.dvorak@email.cz'],
        fail_silently=False,
    )