from django.shortcuts import render
import calendar
import locale
from datetime import date
from django.http import JsonResponse

locale.setlocale(locale.LC_TIME, 'czech')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def user_account(request):
    return render(request, 'user_account.html')

def user_settings(request):
    return render(request, 'user_settings.html')

def user_favorite(request):
    return render(request, 'user_favorite.html')

def reservation_system(request):
    today = date.today()
    year = int(request.GET.get("year", date.today().year))
    month = int(request.GET.get("month", date.today().month))
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            "year": year,
            "month": month,
            "month_name": calendar.month_name[month].capitalize(),
            "weeks": month_days,
            "today_day": today.day,
            "today_month": today.month,
            "today_year": today.year
        })
    else:
        context = {
            "year": year,
            "month": month,
            "month_name": calendar.month_name[month].capitalize(),
            "month_days": month_days,
            "today_day": today.day,
            "today_month": today.month,
            "today_year": today.year
        }
    return render(request, 'reservation_system.html', context)

def organizational_structure(request):
    return render(request, 'organizational_structure.html')

def personnel_records(request):
    return render(request, 'personnel_records_table.html')

def properties_table(request):
    return render(request, 'properties_table.html')

def rooms_table(request):
    return render(request, 'rooms_table.html')

def vehicles_table(request):
    return render(request, 'vehicles_table.html')

def internal_guidelines(request):
    return render(request, 'internal_guidelines.html')

def submit_certificate(request):
    return render(request, 'submit_certificate.html')




