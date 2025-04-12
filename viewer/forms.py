from django.core.validators import validate_email
from django.forms import ModelForm, DateInput, Field

from kamiladmin.settings import DEBUG
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from datetime import date
from django import forms

from .models import *


class WorkExperienceForm(forms.Form):
    initial_creditable_work_experience_years = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(101)],  # 0 až 100 let
        label="Započitatelná doba praxe - roky",
        required=False
    )
    initial_creditable_work_experience_months = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(12)],  # 0 až 11 měsíců
        label="Započitatelná doba praxe - měsíce",
        required=False
    )
    initial_creditable_work_experience_days = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(31)],  # 0 až 30 dní
        label="Započitatelná doba praxe - dny",
        required=False
    )


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
            'type_of_employment': 'Druh pracovního poměru',
            'image': 'Fotografie'
        }

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'start_date_of_employment': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'contract_from': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'contract_until': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'personal_number': forms.NumberInput(attrs={'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        date_fields = ['date_of_birth', 'start_date_of_employment', 'contract_from', 'contract_until']
        for field in date_fields:
            self.fields[field].input_formats = ['%Y-%m-%d']

    def clean_personal_number(self):
        number = self.cleaned_data.get('personal_number')
        if number is not None and number <= 0:
            raise forms.ValidationError('Osobní číslo musí být větší než 0.')
        return number

    def clean_name(self):
        initial = self.cleaned_data.get('name')
        result = initial
        if initial:
            result = initial.capitalize()
        return result

    def clean_surname(self):
        initial = self.cleaned_data.get('surname')
        result = initial
        if initial:
            result = initial.capitalize()
        return result

    def clean_date_of_birth(self):
        initial = self.cleaned_data.get('date_of_birth')
        if DEBUG:
            print(f"initial date of birth: '{initial}'")
        if initial and initial > date.today():
            raise ValidationError("Datum narození nesmí být v budoucnosti")
        return initial

    def clean(self):
        cleaned_data = super().clean()
        initial_name = cleaned_data.get('name')
        initial_surname = cleaned_data.get('surname')
        if DEBUG:
            print(f"initial_name = '{initial_name}', "
                  f"initial_surname = '{initial_surname}'")
        if not initial_name and not initial_surname:
            raise ValidationError("Je nutné zadat jméno a příjmení.")
        return cleaned_data

def section_view(request):
    print("METHOD:", request.method)
    print("POST:", request.POST)
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

def calculate_total_creditable_work_experience(employee):
    current_date = date.today()
    days_since_start = (current_date - employee.start_date_of_employment).days
    total_creditable_work_experience = ((employee.total_initial_creditable_work_experience_in_days() + days_since_start)) // 365
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
        (32, float('inf'), 'other')
    ]

    for lower_bound, upper_bound, section in sections:
        if lower_bound <= value < upper_bound:
            return section, section_data.get(section, [])

    return 'unknown', []

class AgreementWorkerForm(forms.ModelForm):
    class Meta:
        model = AgreementWorker
        fields = ['name', 'surname', 'title_before_name', 'title_after_name', 'date_of_birth',
                  'place_of_birth', 'address', 'email', 'phone_number', 'type_of_agreement',
                  'contract_from', 'contract_until', 'hourly_wage']

    def clean_hourly_wage(self):
        hourly_wage = self.cleaned_data.get('hourly_wage')
        if hourly_wage <= 0:
            raise forms.ValidationError("Hodinová mzda musí být kladná.")
        return hourly_wage

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError("Zadejte platnou e-mailovou adresu.")
        return email

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


class PersonalCompetenceModelForm(ModelForm):
    class Meta:
        model = PersonalCompetence
        fields = '__all__'

        labels = {
            'name': 'Název a typ požadovaného vzdělání/kurzu'
        }


class EmployeePersonalCompetenceForm(forms.ModelForm):
    class Meta:
        model = EmployeePersonalCompetence
        fields = ['competence', 'certificate', 'valid_until']

    certificate = forms.FileField(required=False, label='Certifikát')  # Umožní nahrání souboru certifikátu
    valid_until = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))  # Platnost certifikátu


class CertificateUploadForm(forms.ModelForm):
    class Meta:
        model = EmployeePersonalCompetence
        fields = ['certificate']


class InternalDirectivesModelForm(ModelForm):
    class Meta:
        model = InternalDirectives
        fields = '__all__'

    labels = {
        'type': 'Druh předpisu',
        'name': 'Název směrnice/předpisu',
        'effective_date': 'Datum účinnosti předpisu od:'
    }

    widgets = {
        'effective_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
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
