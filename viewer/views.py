from django.shortcuts import render, redirect, get_object_or_404
import calendar
import locale
from datetime import date
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

locale.setlocale(locale.LC_TIME, 'czech')
from viewer.models import *

def home(request):
    return render(request, 'home.html')

def employees(request):
    employees_ = Employee.objects.all()
    context = {'employees': employees_}
    return render(request=request,
                  template_name="employees.html",
                  context=context)

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
    starosta = Employee.objects.filter(job_position__name__iexact="Starosta").first()
    tajemnik = Employee.objects.filter(job_position__name__iexact="Tajemník").first()
    vedouci_odboru_vnitrni_spravy = Employee.objects.filter(job_position__name__iexact="Vedoucí odboru vnitřní správy").first()
    asistentka_tajemnika = Employee.objects.filter(job_position__name__iexact="Asistentka starosty a tajemníka").first()
    vedouci_odboru_ekonomiky = Employee.objects.filter(job_position__name__iexact="Vedoucí odboru ekonomiky a správy majetku").first()
    referent_spravy_majetku_1 = Employee.objects.filter(job_position__name__iexact="Referent správy majetku 1").first()
    referent_spravy_majetku_2 = Employee.objects.filter(job_position__name__iexact="Referent správy majetku 2").first()
    referent_pokladna = Employee.objects.filter(job_position__name__iexact="Referent-pokladna").first()
    vedouci_oddeleni_ekonomiky = Employee.objects.filter(job_position__name__iexact="Vedoucí oddělení ekonomiky").first()
    ucetni = Employee.objects.filter(job_position__name__iexact="účetní").first()
    return render(request, 'organizational_structure.html', {'starosta': starosta,
                                                             'tajemnik': tajemnik,
                                                             'vedouci_odboru_vnitrni_spravy': vedouci_odboru_vnitrni_spravy,
                                                             'asistentka_tajemnika': asistentka_tajemnika,
                                                             'vedouci_odboru_ekonomiky': vedouci_odboru_ekonomiky,
                                                             'referent_spravy_majetku_1': referent_spravy_majetku_1,
                                                             'referent_spravy_majetku_2': referent_spravy_majetku_2,
                                                             'vedouci_oddeleni_ekonomiky': vedouci_oddeleni_ekonomiky,
                                                             'referent_pokladna': referent_pokladna,
                                                             'ucetni': ucetni,})

def personnel_records(request):
    employees = Employee.objects.all()
    return render(request, 'personnel_records_table.html', {'employees': employees})

def employee_detail(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees_detail.html', {'emp': emp})

def employee_create(request):
    if request.method == 'POST':
        print("Formulář byl odeslán")
        form = EmployeeModelForm(request.POST)
        if form.is_valid():
            print("Formulář je validní")
            form.save()
            return redirect('personnel_records')
        else:
            print("Formulář není validní")
            print(form.errors)
    else:
        form = EmployeeModelForm()
    return render(request, 'employee_form.html', {'form': form, 'action': 'Vytvořit'})


def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeModelForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('personnel_records')
    else:
        form = EmployeeModelForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form, 'action': 'Upravit'})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('personnel_records')
    return render(request, 'employee_confirm_delete.html', {'employee': employee})

def vehicle_create(request):
    if request.method == 'POST':
        print("Formulář byl odeslán")
        form = CarsModelForm(request.POST)
        if form.is_valid():
            print("Formulář je validní")
            form.save()
            return redirect('vehicles_table')
        else:
            print("Formulář není validní")
            print(form.errors)
    else:
        form = CarsModelForm()
    return render(request, 'vehicle_form.html', {'form': form, 'action': 'Vytvořit'})

def vehicle_update(request, pk):
    vehicle = get_object_or_404(Cars, pk=pk)
    if request.method == 'POST':
        form = CarsModelForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicles_table')
    else:
        form = CarsModelForm(instance=vehicle)
    return render(request, 'vehicle_form.html', {'form': form, 'action': 'Upravit'})

def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Cars, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicles_table')
    return render(request, 'vehicle_confirm_delete.html', {'vehicle': vehicle})

def property_create(request):
    if request.method == 'POST':
        print("Formulář byl odeslán")
        form = RealEstatesModelForm(request.POST)
        if form.is_valid():
            print("Formulář je validní")
            form.save()
            return redirect('properties_table')
        else:
            print("Formulář není validní")
            print(form.errors)
    else:
        form = RealEstatesModelForm()
    return render(request, 'property_form.html', {'form': form, 'action': 'Vytvořit'})

def property_update(request, pk):
    property = get_object_or_404(RealEstates, pk=pk)
    if request.method == 'POST':
        form = RealEstatesModelForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('properties')
    else:
        form = RealEstatesModelForm(instance=property)
    return render(request, 'property_form.html', {'form': form, 'action': 'Upravit'})

def property_delete(request, pk):
    property = get_object_or_404(RealEstates, pk=pk)
    if request.method == 'POST':
        property.delete()
        return redirect('properties')
    return render(request, 'property_confirm_delete.html', {'property': property})


def properties_table(request):
    properties = RealEstates.objects.all()
    return render(request, 'properties_table.html', {'properties': properties})

def properties_detail(request, pk):
    prop = get_object_or_404(RealEstates, pk=pk)
    return render(request, 'properties_detail.html', {'prop': prop})

def rooms_table(request):
    rooms = [
        {
            "name": ""
        }
    ]
    return render(request, 'rooms_table.html')

def vehicles_table(request):
    vehicles = Cars.objects.all()
    return render(request, 'vehicles_table.html', {"cars": vehicles})

def vehicle_detail(request, pk):
    car = get_object_or_404(Cars, pk=pk)
    return render(request, 'vehicle_detail.html', {"car": car})

def internal_directives(request):
    directives = InternalDirectives.objects.all()
    return render(request, 'internal_directives.html', {'directives': directives})

def directive_create(request):
    if request.method == 'POST':
        form = InternalDirectivesModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('internal_directives')
    else:
        form = InternalDirectivesModelForm()
    return render(request, 'directive_form.html', {'form': form, 'action': 'Nahrát'})

def directive_update(request, pk):
    directive = get_object_or_404(InternalDirectives, pk=pk)
    if request.method == 'POST':
        form = InternalDirectivesModelForm(request.POST, request.FILES, instance=directive)
        if form.is_valid():
            form.save()
            return redirect('internal_directives')
    else:
        form = InternalDirectivesModelForm(instance=directive)
    return render(request, 'directive_form.html', {'form': form, 'action': 'Upravit'})

def directive_delete(request, pk):
    directive = get_object_or_404(InternalDirectives, pk=pk)
    if request.method == 'POST':
        directive.delete()
        return redirect('internal_directives')
    return render(request, 'directive_confirm_delete.html', {'directive': directive})

def directive_detail(request, pk):
    directive = get_object_or_404(InternalDirectives, pk=pk)
    return render(request, 'directive_detail.html', {"directive": directive})