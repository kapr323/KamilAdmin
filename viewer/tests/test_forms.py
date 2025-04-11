import pytest
from viewer.forms import (EmployeeModelForm, calculate_total_creditable_work_experience, assign_salary_grade_step,
                          JobPositionModelForm)
from viewer.models import JobPosition, Employee, PersonalCompetence
from datetime import date, timedelta

@pytest.mark.django_db
def test_employee_form_valid_data():
    job = JobPosition.objects.create(name="Tester")
    form_data = {
        'name': 'karel',
        'surname': 'novák',
        'personal_number': 123,
        'job_position': job.pk,
        'date_of_birth': '1990-01-01',
        'place_of_birth': 'Brno',
        'nationality': 'Česká',
        'address': 'Testovací 123',
        'email': 'test@example.com',
        'start_date_of_employment': '2020-01-01',
        'contract_from': '2020-01-01',
        'contract_until': '2025-01-01',
        'education_level': 'Střední vzdělání s maturitou',
        'type_of_employment': 'Hlavní pracovní poměr',
        'initial_creditable_work_experience_years': 0,
        'initial_creditable_work_experience_months': 0,
        'initial_creditable_work_experience_days': 0,
        'image': None,

    }
    form = EmployeeModelForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_employee_form_invalid_email():
    job = JobPosition.objects.create(name="Tester")
    form_data = {
        'name': 'karel',
        'surname': 'novák',
        'personal_number': 123,
        'job_position': job.pk,
        'date_of_birth': '1990-01-01',
        'place_of_birth': 'Brno',
        'nationality': 'Česká',
        'address': 'Testovací 123',
        'email': 'neplatny-email',
        'start_date_of_employment': '2020-01-01',
        'contract_from': '2020-01-01',
        'contract_until': '2025-01-01',
        'education_level': 'Střední vzdělání s maturitou',
        'type_of_employment': 'Hlavní pracovní poměr',
    }
    form = EmployeeModelForm(data=form_data)
    assert not form.is_valid()
    assert 'email' in form.errors

@pytest.mark.django_db
def test_employee_form_future_birth_date():
    job = JobPosition.objects.create(name="Tester")
    future_date = date.today().replace(year=date.today().year + 1)
    form_data = {
        'name': 'karel',
        'surname': 'novák',
        'personal_number': 123,
        'job_position': job.pk,
        'date_of_birth': future_date.strftime('%Y-%m-%d'),
        'place_of_birth': 'Brno',
        'nationality': 'Česká',
        'address': 'Testovací 123',
        'email': 'test@example.com',
        'start_date_of_employment': '2020-01-01',
        'contract_from': '2020-01-01',
        'contract_until': '2025-01-01',
        'education_level': 'Střední vzdělání s maturitou',
        'type_of_employment': 'Hlavní pracovní poměr',
        'initial_creditable_work_experience_years': 0,
        'initial_creditable_work_experience_months': 0,
        'initial_creditable_work_experience_days': 0,
        'image': None,
    }
    form = EmployeeModelForm(data=form_data)
    assert not form.is_valid()
    assert 'date_of_birth' in form.errors

@pytest.mark.django_db
def test_employee_form_invalid_personal_number():
    job = JobPosition.objects.create(name="Tester")
    form_data = {
        'name': 'karel',
        'surname': 'novák',
        'personal_number': -1,
        'job_position': job.pk,
        'date_of_birth': '1990-01-01',
        'place_of_birth': 'Brno',
        'nationality': 'Česká',
        'address': 'Testovací 123',
        'email': 'test@example.com',
        'start_date_of_employment': '2020-01-01',
        'contract_from': '2020-01-01',
        'contract_until': '2025-01-01',
        'education_level': 'Střední vzdělání s maturitou',
        'type_of_employment': 'Hlavní pracovní poměr',
        'initial_creditable_work_experience_years': 0,
        'initial_creditable_work_experience_months': 0,
        'initial_creditable_work_experience_days': 0,
        'image': None,
    }
    form = EmployeeModelForm(data=form_data)
    assert not form.is_valid()
    assert 'personal_number' in form.errors

@pytest.mark.django_db
def test_employee_form_name_capitalization():
    job = JobPosition.objects.create(name="Tester")
    form_data = {
        'name': 'karel',
        'surname': 'novák',
        'personal_number': 456,
        'job_position': job.pk,
        'date_of_birth': '1990-01-01',
        'place_of_birth': 'Brno',
        'nationality': 'Česká',
        'address': 'Testovací 123',
        'email': 'test@example.com',
        'start_date_of_employment': '2020-01-01',
        'contract_from': '2020-01-01',
        'contract_until': '2025-01-01',
        'education_level': 'Střední vzdělání s maturitou',
        'type_of_employment': 'Hlavní pracovní poměr',
        'initial_creditable_work_experience_years': 0,
        'initial_creditable_work_experience_months': 0,
        'initial_creditable_work_experience_days': 0,
        'image': None,
    }
    form = EmployeeModelForm(data=form_data)
    form.is_valid()
    assert form.cleaned_data['name'] == 'Karel'
    assert form.cleaned_data['surname'] == 'Novák'

@pytest.mark.django_db
def test_employee_form_empty_name_and_surname():
    job = JobPosition.objects.create(name="Tester")
    form_data = {
        'name': '',
        'surname': '',
        'personal_number': 123,
        'job_position': job.pk,
        'date_of_birth': '1990-01-01',
        'place_of_birth': 'Brno',
        'nationality': 'Česká',
        'address': 'Testovací 123',
        'email': 'test@example.com',
        'start_date_of_employment': '2020-01-01',
        'contract_from': '2020-01-01',
        'contract_until': '2025-01-01',
        'education_level': 'Střední vzdělání s maturitou',
        'type_of_employment': 'Hlavní pracovní poměr',
        'initial_creditable_work_experience_years': 0,
        'initial_creditable_work_experience_months': 0,
        'initial_creditable_work_experience_days': 0,
        'image': None,
    }
    form = EmployeeModelForm(data=form_data)
    assert not form.is_valid()
    assert '__all__' in form.errors

@pytest.mark.django_db
def test_employee_form_invalid_personal_number_zero():
    job = JobPosition.objects.create(name="Tester")
    form_data = {
        'name': 'Jan',
        'surname': 'Novák',
        'personal_number': 0,  # ✖ neplatné číslo
        'job_position': job.pk,
        'date_of_birth': '1990-01-01',
        'place_of_birth': 'Brno',
        'nationality': 'Česká',
        'address': 'Test 123',
        'email': 'jan@example.com',
        'start_date_of_employment': '2020-01-01',
        'contract_from': '2020-01-01',
        'contract_until': '2025-01-01',
        'education_level': 'Střední',
        'type_of_employment': 'Hlavní pracovní poměr',
        'initial_creditable_work_experience_years': 0,
        'initial_creditable_work_experience_months': 0,
        'initial_creditable_work_experience_days': 0,
    }
    form = EmployeeModelForm(data=form_data)
    assert not form.is_valid()
    assert 'personal_number' in form.errors

@pytest.mark.django_db
def test_calculate_total_creditable_work_experience():
    job = JobPosition.objects.create(name="Tester")

    emp = Employee.objects.create(
        name="Anna", surname="Jantarová", personal_number=4487,
        date_of_birth=date(1990, 10, 11), place_of_birth="Pálava", nationality="CZ",
        address="Hroznová 34", email="a@b.cd",
        start_date_of_employment=date.today() - timedelta(days=365 * 3),
        contract_from=date.today() - timedelta(days=365 * 3),
        contract_until=date.today() + timedelta(days=365),
        job_position=job,
        initial_creditable_work_experience_years=2,
        initial_creditable_work_experience_months=0,
        initial_creditable_work_experience_days=0
    )

    result = calculate_total_creditable_work_experience(emp)

    assert result == 5

def test_assign_salary_grade_step():
    assert assign_salary_grade_step(0.5)[0] == '1'
    assert assign_salary_grade_step(1.5)[0] == '2'
    assert assign_salary_grade_step(7.5)[0] == '5'
    assert assign_salary_grade_step(32.1)[0] == 'other'
    assert assign_salary_grade_step(-1)[0] == 'unknown'
    assert assign_salary_grade_step(100)[0] == 'other'


@pytest.mark.django_db
def test_job_position_form_clean_name():
    competence = PersonalCompetence.objects.create(name="Test kompetence", valid_until="2030-01-01")

    form_data = {
        'name': 'tester',
        'grade': 8,
        'personal_competencies': [competence.pk],
    }
    form = JobPositionModelForm(data=form_data)

    assert form.is_valid()
    assert form.cleaned_data['name'] == 'Tester'