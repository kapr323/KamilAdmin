from django.forms import ModelForm, DateField, NumberInput

from kamiladmin.settings import DEBUG
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from datetime import datetime, date
from django import forms

from viewer.models import *

"""
class Employee(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=False)
    surname = CharField(max_length=32, null=False, blank=False, unique=False)
    title_before_name = CharField(max_length=20, null=True, blank=True, unique=False)
    title_after_name = CharField(max_length=20, null=True, blank=True, unique=False)
    personal_number = IntegerField(null=False, blank=True, unique=True)
    job_position = ForeignKey("JobPosition", null=True, blank=False, unique=False, on_delete=SET_NULL, related_name='employee_job_position')
    date_of_birth = DateField(null=False, blank=False, unique=False)
    place_of_birth = CharField(max_length=40, null=False, blank=False, unique=False)
    nationality = CharField(max_length=20, null=False, blank=False, unique=False)
    address = CharField(max_length=100, null=False, blank=False, unique=False)
    start_date_of_employment = DateField(null=False, blank=False, unique=False)
    contract_from = DateField(null=False, blank=False, unique=False, default=None)
    contract_until = DateField(null=False, blank=False, unique=False, default=None)
    initial_creditable_work_experience_years = models.PositiveIntegerField(default=0)
    initial_creditable_work_experience_months = models.PositiveIntegerField(default=0,
                                                                            choices=[(i, str(i)) for i in range(12)])
    initial_creditable_work_experience_days = models.PositiveIntegerField(default=0,
                                                                          choices=[(i, str(i)) for i in range(31)])
    education_level = CharField(max_length=20, null=False, blank=False, unique=False)
    type_of_employment = CharField(max_length=20, null=False, blank=False, unique=False)
"""


class EmployeeModelForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

        labels = {
            'name': 'Jméno',
            'surname': 'Příjmení',
            'title_before_name': 'Titul před jménem',
            'title_after_name': 'Titul za jménem',
            'personal_number': 'Osobní číslo',
            'job_position': 'Název pozice',
            'date_of_birth': 'Datum narození',
            'place_of_death': 'Místo narození',
            'nationality': 'Národnost',
            'address': 'Adresa trvalého bydliště',
            'email': 'E-mail',
            'start_date_of_employment': 'Datum nástupu',
            'contract_from': 'Platost smlouvy od',
            'contract_until': 'Platost smlouvy do',
            'initial_creditable_work_experience_years': 'Počet let započitatelné praxe',
            'initial_creditable_work_experience_months': 'Počet měsíců započitatelné praxe',
            'initial_creditable_work_experience_days': 'Počet let započitatelné days',
            'education_level': 'Maximální dosažené vzdělání',
            'type_of_employment': 'Druh pracovního poměru'
            }

    def clean_name(self):
        initial = self.cleaned_data['name']
        result = initial
        if initial:
            result = initial.capitalize()
        return result

    def clean_surname(self):
        initial = self.cleaned_data['surname']
        result = initial
        if initial:
            result = initial.capitalize()
        return result

    def clean_date_of_birth(self):
        initial = self.cleaned_data['date_of_birth']
        if DEBUG:
            print(f"initial date of birth: '{initial}'")
        if initial and initial > date.today():
            raise ValidationError("Datum narození nesmí být v budoucnosti")
        return initial

    def clean(self):
        cleaned_data = super().clean()
        initial_name = cleaned_data['name']
        initial_surname = cleaned_data['surname']
        if DEBUG:
            print(f"initial_name = '{initial_name}', "
                  f"initial_surname = '{initial_surname}'")
        if not initial_name and not initial_surname:
            raise ValidationError("Je nutné zadat jméno a příjmení.")
        return cleaned_data


def calculate_total_creditable_work_experience(employee):
    current_date = datetime.now()
    days_since_start = (current_date - employee.start_date_of_employment).days
    total_creditable_work_experience = ((employee.total_initial_experience_in_days()) + days_since_start) // 365
    return total_creditable_work_experience


section_data = {
    '1': ['step1'],
    '2': ['step2'],
    '3': ['step3'],
    '4': ['step4'],
    '5': ['step5'],
    '6': ['step6'],
    '7': ['step7'],
    '8': ['step8'],
    '9': ['step9'],
    '10': ['step10'],
    '11': ['step11'],
    '12': ['step12']
}

def assign_salary_grade_step(value):
    sections = [
        (0, 1, '1'),
        (1, 2, '2'),
        (2, 4, '3'),
        (4, 6, '4'),
        (6, 9, '5'),
        (9, 12, '6'),
        (12, 15, '7'),
        (15, 19, '8'),
        (19, 23, '9'),
        (23, 27, '10'),
        (27, 32, '11'),
        (32, float('12'), 'other')
    ]# Pro jakékoli větší hodnoty

    for lower_bound, upper_bound, section in sections:
        if lower_bound <= value < upper_bound:
            return section, section_data.get(section, [])

    return 'unknown', []


def section_view(request):
    if request.method == 'POST':
        form = EmployeeModelForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            total_creditable_work_experience = calculate_total_creditable_work_experience(employee)
            section, fields = assign_salary_grade_step(total_creditable_work_experience)
            return JsonResponse({'total_creditable_work_experience': total_creditable_work_experience, 'section': section, 'fields': fields})
    else:
        form = EmployeeModelForm()
    return JsonResponse({'error': 'Invalid input or method.'}, status=400)


class JobPositionModelForm(ModelForm):
    class Meta:
        model = JobPosition
        fields = '__all__'

        labels = {
            'name': 'Název pozice'
        }

    def clean_name(self):
        initial = self.cleaned_data['name']
        return initial.capitalize()


class SalaryModelForm(ModelForm):
    class Meta:
        model = SalaryGrade
        fields = '__all__'

        labels = {
            'grade': 'Platová třída',
            'step': 'Platový stupeň'
        }


class ContractModelForm(ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'

        labels = {
            'name': 'Druh pracovního poměru'
        }


class PersonalCompetenceModelForm(ModelForm):
    class Meta:
        model = PersonalCompetence
        fields = '__all__'

        labels = {
            'name': 'Název a typ požadovaného vzdělání/kurzu'
        }


    class InternalDirectivesModelForm(ModelForm):
        class Meta:
            model = InternalDirectives
            fields = '__all__'

        labels = {
            'name': 'Název směrnice/předpisu',
            'effective_date': 'Datum účinnosti předpisu od:'
        }


    class CarsModelForm(ModelForm):
        class Meta:
            model = Cars
            fields = '__all__'

        labels = {
            'name': 'Tovární značka vozidla',
            'type': 'Typ',
            'plate_number': 'Registrační značka vozidla',
            'fuel_type': 'Typ paliva',
            'technical_inspection_date': 'Datum příští technické prohlídky',
            'highway_ticket_validity': 'Dálniční známka platná do:',
            'is_usable': 'Je použitelné (není v servisu, nepojízdné, apod.)'
        }


class RealEstatesModelForm(ModelForm):
    class Meta:
        model = RealEstates
        fields = '__all__'

    labels = {
        'name': 'Název nemovitosti',
        'type': 'Typ',
        'address': 'Adresa',
        'is_usable': 'Je použitelná'
    }
