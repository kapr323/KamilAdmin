from celery import shared_task
from django.core.mail import send_mail
from datetime import date
from models import Employee

@shared_task
def send_work_anniversary_email():
    """
    Posílá e-maily zaměstnancům k pracovnímu výročí.
    TODO: nutno nastavit emailovou adresu pro odesílání
    """
    today = date.today()
    employees = Employee.objects.filter(start_date_of_employment__month=today.month, start_date_of_employment__day=today.day)

    for employee in employees:
        send_mail(
            subject="Gratulujeme k pracovnímu výročí! 🎉",
            message=f"Ahoj {employee.name},\n\nDnes slavíš {today.year - employee.start_date_of_employment.year}. pracovní výročí! 🎉",
            from_email="noreply@firma.cz",
            recipient_list=[employee.email],
            fail_silently=False,
        )

    return f"Emails sent to {len(employees)} employees"