from django.shortcuts import render, redirect, get_object_or_404
import calendar
import locale

from .forms import *


locale.setlocale(locale.LC_TIME, 'czech')
from viewer.models import *
from django.shortcuts import render, redirect
from .forms import EmployeeModelForm


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

def personnel_management(request):
    return render(request, 'personnel_management.html')

def properties(request):
    return render(request, 'properties.html')

def vehicles(request):
    return render(request, 'vehicles.html')

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
        ('ucetni', "Účetní"),
    ]
    return render(request, 'organizational_structure.html', context = {key: Employee.objects.filter(job_position__name__iexact=label).first() for key, label in positions}
)

def personnel_records(request):
    # Zobrazíme zaměstnance s hlavním pracovním poměrem nebo částečným pracovním úvazkem
    employees = Employee.objects.filter(type_of_employment__in=[
        Employee.TypeOfEmployment.MAIN_EMPLOYMENT_RELATIONSHIP,
        Employee.TypeOfEmployment.PART_TIME_JOB,
        Employee.TypeOfEmployment.VACANT_REPRESENTATIVE
    ])
    return render(request, 'personnel_records_table.html', {'employees': employees})

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    position_competencies = employee.job_position.personal_competencies.all()

    competencies_data = []

    for comp in position_competencies:
        epc = EmployeePersonalCompetence.objects.filter(employee=employee, competence=comp).first()

        if not epc:
            epc = EmployeePersonalCompetence(
                employee=employee,
                competence=comp,  # klíčové – aby se dalo z `competence.pk` brát ID!
                certificate=None
            )

        competencies_data.append(epc)

    return render(request, 'employees_detail.html', {
        'employee': employee,
        'competencies': competencies_data,
    })


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


def add_employee(request):
    if request.method == 'POST':
        form = EmployeeModelForm(request.POST)
        if form.is_valid():
            form.save()  # Uloží nový záznam zaměstnance
            return redirect('personnel_records_table')  # Po uložení přesměruje na seznam
    else:
        form = EmployeeModelForm()

    return render(request, 'add_employee.html', {'form': form})


def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return process_form(
        request,
        form_class=EmployeeModelForm,
        template='employee_form.html',
        redirect_url='personnel_records_table',
        instance=employee,
        action='Upravit'
    )

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return process_delete(
        request=request,
        instance=employee,
        template='employee_confirm_delete.html',
        redirect_url='personnel_records_table',
        context_name='employee'
    )


def add_employee_view(request):
    form = WorkExperienceForm(request.POST or None)

    if form.is_valid():
        years = form.cleaned_data.get('initial_creditable_work_experience_years')
        months = form.cleaned_data.get('initial_creditable_work_experience_months')
        days = form.cleaned_data.get('initial_creditable_work_experience_days')

    return render(request, 'add_employee.html', {'form': form})


def upload_employee_certificate(request, employee_pk, competence_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    competence = get_object_or_404(PersonalCompetence, pk=competence_pk)

    employee_competence, created = EmployeePersonalCompetence.objects.get_or_create(
        employee=employee,
        competence=competence
    )

    if request.method == 'POST' and 'certificate' in request.FILES:
        employee_competence.certificate = request.FILES['certificate']
        employee_competence.save()

        print(f"Certifikát uložen pro {employee} – {competence.name}")

        return redirect('employee_detail', pk=employee.pk)

    return render(request, 'upload_employee_certificate.html', {
        'employee': employee,
        'competence': competence
    })


# Zobrazení pro seznam pracovníků s dohodami (DPČ/DPP)
def agreement_workers_list(request):
    # Načti všechny pracovníky na dohodu
    workers = AgreementWorker.objects.all()
    return render(request, 'agreement_workers_list.html', {'workers': workers})

# Přidání pracovníka s dohodou
def add_agreement_worker(request):
    if request.method == 'POST':
        form = AgreementWorkerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agreement_workers_list')
    else:
        form = AgreementWorkerForm()
    return render(request, 'add_agreement_worker.html', {'form': form})


def agreement_worker_detail(request, pk):
    worker = get_object_or_404(AgreementWorker, pk=pk)
    return render(request, 'agreement_worker_detail.html', {'worker': worker})


# Aktualizace pracovníka s dohodou
def agreement_worker_update(request, pk):
    worker = get_object_or_404(AgreementWorker, pk=pk)
    if request.method == 'POST':
        form = AgreementWorkerForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            return redirect('agreement_workers_list')
    else:
        form = AgreementWorkerForm(instance=worker)

    return render(request, 'add_agreement_worker.html', {'form': form, 'action': 'Upravit'})


# Smazání pracovníka s dohodou
def agreement_worker_delete(request, pk):
    worker = get_object_or_404(AgreementWorker, pk=pk)
    return process_delete(
        request=request,
        instance=worker,
        template='agreement_worker_confirm_delete.html',
        redirect_url='agreement_workers_list',
        context_name='worker'
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


def upload_internal_directive(request, pk):
    directive = get_object_or_404(InternalDirectives, pk=pk)

    # Zpracování nahrání dokumentu
    if request.method == 'POST' and 'document' in request.FILES:
        directive.document = request.FILES['document']
        directive.save()

        return redirect('internal_directive_detail', pk=directive.pk)

    return render(request, 'upload_internal_directives.html', {'directive': directive})


def directive_create(request):
    return process_form(
        request,
        form_class=InternalDirectivesModelForm,
        template='directive_form.html',
        redirect_url='internal_directive_list',
        action='Nahrát'
    )

def directive_update(request, pk):
    directive = get_object_or_404(InternalDirectives, pk=pk)
    return process_form(
        request,
        form_class=InternalDirectivesModelForm,
        template='directive_form.html',
        redirect_url='internal_directive_list',
        instance=directive,
        action='Upravit'
    )

def directive_delete(request, pk):
    directive = get_object_or_404(InternalDirectives, pk=pk)
    return process_delete(
        request,
        instance=directive,
        template='directive_confirm_delete.html',
        redirect_url='internal_directive_list',
        context_name='directive'
    )

def directive_detail(request, pk):
    directive = get_object_or_404(InternalDirectives, pk=pk)
    return render(request, 'directive_detail.html', {"directive": directive})