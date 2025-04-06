from django.shortcuts import render, redirect, get_object_or_404
import calendar
import locale
from datetime import date
from django.http import JsonResponse
from .forms import InternalDirectivesModelForm, CarsModelForm, RealEstatesModelForm, EmployeeModelForm

locale.setlocale(locale.LC_TIME, 'czech')
from viewer.models import InternalDirectives, Cars, RealEstates, Employee

def get_calendar(request):
    today = date.today()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)

    data = {
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month].capitalize(),
        "month_days": month_days,
        "selected_day": today.day,
        "selected_month": today.month,
        "selected_year": today.year
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            "year": data["year"],
            "month": data["month"],
            "month_name": data["month_name"],
            "weeks": data["month_days"],
            "selected_day": data["selected_day"],
            "selected_month": data["selected_month"],
            "selected_year": data["selected_year"]
        })

    return data

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

def properties_reservations(request):
    calendar_data = get_calendar(request)
    if isinstance(calendar_data, JsonResponse):
        return calendar_data
    calendar_data['properties'] = RealEstates.objects.all()
    return render(request, 'properties_reservations.html', calendar_data)

def vehicles_reservations(request):
    calendar_data = get_calendar(request)
    if isinstance(calendar_data, JsonResponse):
        return calendar_data
    calendar_data['vehicles'] = Cars.objects.all()
    return render(request, 'vehicles_reservations.html', calendar_data)

def organizational_structure(request):
    positions = [
        ('starosta', "Starosta"),
        ('tajemnik', "Tajemník"),
        ('asistentka_tajemnika', "Asistentka starosty a tajemníka"),
        ('vedouci_odboru_ekonomiky', "Vedoucí odboru ekonomiky a správy majetku"),
        ('referent_spravy_majetku_1', "Referent správy majetku 1"),
        ('referent_spravy_majetku_2', "Referent správy majetku 2"),
        ('referent_pokladna', "Referent-pokladna"),
        ('vedouci_oddeleni_ekonomiky', "Vedoucí oddělení ekonomiky"),
        ('vedouci_odboru_vnitrni_spravy', "Vedoucí odboru vnitřní správy"),
        ('ucetni', "účetní")
    ]
    return render(request, 'organizational_structure.html', context = {key: Employee.objects.filter(job_position__name__iexact=label).first() for key, label in positions}
)

def personnel_records(request):
    employees = Employee.objects.all()
    return render(request, 'personnel_records_table.html', {'employees': employees})

def employee_detail(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees_detail.html', {'emp': emp})

def process_form(request, form_class, template, redirect_url, instance=None, action="Uložit"):
    form = form_class(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(redirect_url)
    return render(request, template, {'form': form, 'action': action})

def process_delete(request, instance, template, redirect_url, context_name):
    if request.method == 'POST':
        instance.delete()
        return redirect(redirect_url)
    return render(request, template, {context_name: instance})


def employee_create(request):
    return process_form(
        request,
        form_class=EmployeeModelForm,
        template='employee_form.html',
        redirect_url='personnel_records',
        action='Vytvořit'
    )

def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return process_form(
        request,
        form_class=EmployeeModelForm,
        template='employee_form.html',
        redirect_url='personnel_records',
        instance=employee,
        action='Upravit'
    )

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return process_delete(
        request=request,
        instance=employee,
        template='employee_confirm_delete.html',
        redirect_url='personnel_records',
        context_name='employee'
    )

def vehicle_create(request):
    return process_form(
        request,
        form_class=CarsModelForm,
        template='vehicle_form.html',
        redirect_url='vehicles_table',
        action='Vytvořit'
    )

def vehicle_update(request, pk):
    vehicle = get_object_or_404(Cars, pk=pk)
    return process_form(
        request,
        form_class=CarsModelForm,
        template='vehicle_form.html',
        redirect_url='vehicles_table',
        instance=vehicle,
        action='Upravit'
    )

def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Cars, pk=pk)
    return process_delete(
        request,
        instance=vehicle,
        template='vehicle_confirm_delete.html',
        redirect_url='vehicles_table',
        context_name='vehicle'
    )

def property_create(request):
    return process_form(
        request,
        form_class=RealEstatesModelForm,
        template='property_form.html',
        redirect_url='properties_table',
        action='Vytvořit'
    )

def property_update(request, pk):
    property_instance = get_object_or_404(RealEstates, pk=pk)
    return process_form(
        request,
        form_class=RealEstatesModelForm,
        template='property_form.html',
        redirect_url='properties_table',
        instance=property_instance,
        action='Upravit'
    )

def property_delete(request, pk):
    property_instance = get_object_or_404(RealEstates, pk=pk)
    return process_delete(
        request,
        instance=property_instance,
        template='property_confirm_delete.html',
        redirect_url='properties_table',
        context_name='property'
    )

def properties_table(request):
    properties = RealEstates.objects.all()
    return render(request, 'properties_table.html', {'properties': properties})

def properties_detail(request, pk):
    prop = get_object_or_404(RealEstates, pk=pk)
    return render(request, 'properties_detail.html', {'prop': prop})

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
    return process_form(
        request,
        form_class=InternalDirectivesModelForm,
        template='directive_form.html',
        redirect_url='internal_directives',
        action='Nahrát'
    )

def directive_update(request, pk):
    directive = get_object_or_404(InternalDirectives, pk=pk)
    return process_form(
        request,
        form_class=InternalDirectivesModelForm,
        template='directive_form.html',
        redirect_url='internal_directives',
        instance=directive,
        action='Upravit'
    )

def directive_delete(request, pk):
    directive = get_object_or_404(InternalDirectives, pk=pk)
    return process_delete(
        request,
        instance=directive,
        template='directive_confirm_delete.html',
        redirect_url='internal_directives',
        context_name='directive'
    )

def directive_detail(request, pk):
    directive = get_object_or_404(InternalDirectives, pk=pk)
    return render(request, 'directive_detail.html', {"directive": directive})

def rooms_table(request):
    rooms = [
        {
            "name": ""
        }
    ]
    return render(request, 'rooms_table.html')