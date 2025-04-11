import pytest
from django.core.exceptions import ValidationError
from viewer.models import (
    Employee, SalaryGrade, JobPosition, PersonalCompetence,
    EmployeePersonalCompetence, InternalDirectives, Cars, RealEstates, validate_phone_number
)
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.django_db
def test_create_employee():
    job = JobPosition.objects.create(name="Testovací pozice")
    emp = Employee.objects.create(
        name="Jan",
        surname="Novák",
        personal_number=1234,
        job_position=job,
        date_of_birth=date(1990, 1, 1),
        place_of_birth="Brno",
        nationality="Česká",
        address="Testovací 123",
        email="test@example.com",
        start_date_of_employment=date(2020, 1, 1),
        contract_from=date(2020, 1, 1),
        contract_until=date(2025, 1, 1)
    )
    assert emp.__str__() == "Jan (Novák) 1234"

@pytest.mark.django_db
def test_salary_grade_str_and_repr():
    grade = SalaryGrade.objects.create(grade=9, step=3)
    assert str(grade) == "9-3"
    assert repr(grade) == "9-3"

@pytest.mark.django_db
def test_job_position_str():
    pos = JobPosition.objects.create(name="Účetní")
    assert str(pos) == "Účetní"

@pytest.mark.django_db
def test_personal_competence_str():
    job = JobPosition.objects.create(name="IT specialista")
    comp = PersonalCompetence.objects.create(name="Práce s počítačem", valid_until=date(2030, 1, 1), job_position=job)
    assert str(comp) == "Práce s počítačem"

@pytest.mark.django_db
def test_employee_personal_competence_fulfilled_property():
    emp = Employee.objects.create(
        name="Anna", surname="Nová", personal_number=5678, date_of_birth=date(1995, 5, 5),
        place_of_birth="Praha", nationality="Česká", address="Ulice 1", email="anna@example.com",
        start_date_of_employment=date(2022, 1, 1), contract_from=date(2022, 1, 1), contract_until=date(2024, 1, 1)
    )
    comp = PersonalCompetence.objects.create(name="Angličtina", valid_until=date(2030, 1, 1))
    cert = SimpleUploadedFile("cert.pdf", b"file_content")
    rel = EmployeePersonalCompetence.objects.create(employee=emp, competence=comp, certificate=cert)
    assert rel.fulfilled is True

@pytest.mark.django_db
def test_internal_directives_repr_and_str():
    directive = InternalDirectives.objects.create(
        name="Bezpečnostní směrnice",
        effective_date=date(2024, 1, 1),
    )
    assert str(directive) == "Bezpečnostní směrnice"

@pytest.mark.django_db
def test_cars_repr_and_str():
    car = Cars.objects.create(
        name="Škoda Octavia", plate_number="1A2 3456",
        technical_inspection_date=date(2025, 5, 5)
    )
    assert str(car) == "Škoda Octavia"
    assert "(Škoda Octavia, 1A2 3456)" in repr(car)

@pytest.mark.django_db
def test_real_estates_repr_and_str():
    estate = RealEstates.objects.create(
        name="Kancelář 1", type="Budova", address="Testovací 99"
    )
    assert str(estate) == "Kancelář 1"

@pytest.mark.django_db
def test_total_initial_creditable_work_experience_in_days():
    job = JobPosition.objects.create(name="Testovací")
    emp = Employee.objects.create(
        name="Eva", surname="Modrá", personal_number=9999, job_position=job,
        date_of_birth=date(1990, 1, 1), place_of_birth="Brno", nationality="Česká",
        address="Ulice", email="e@example.com", start_date_of_employment=date(2020, 1, 1),
        contract_from=date(2020, 1, 1), contract_until=date(2025, 1, 1),
        initial_creditable_work_experience_years=1,
        initial_creditable_work_experience_months=2,
        initial_creditable_work_experience_days=10
    )
    assert emp.total_initial_creditable_work_experience_in_days() == (1 * 365 + 2 * 30 + 10)

def test_validate_phone_number_valid():
    validate_phone_number("+420123456789")  # nevyhodí výjimku = OK

def test_validate_phone_number_invalid():
    with pytest.raises(ValidationError):
        validate_phone_number("123456789")  # chybí +420

@pytest.mark.django_db
def test_employee_repr():
    emp = Employee.objects.create(
        name="Luděk", surname="Kozel", personal_number=1111,
        date_of_birth=date(1985, 6, 6), place_of_birth="Brno", nationality="CZ",
        address="Test 12", email="l@k.cz",
        start_date_of_employment=date(2020, 1, 1),
        contract_from=date(2020, 1, 1), contract_until=date(2025, 1, 1)
    )
    assert repr(emp) == "Luděk Kozel (1111)"

@pytest.mark.django_db
def test_job_position_repr():
    job = JobPosition.objects.create(name="Vedoucí")
    assert repr(job) == "Vedoucí"

@pytest.mark.django_db
def test_job_position_repr():
    job = JobPosition.objects.create(name="Vedoucí")
    assert repr(job) == "Vedoucí"

@pytest.mark.django_db
def test_personal_competence_repr():
    comp = PersonalCompetence.objects.create(name="Zkouška", valid_until=date(2030, 1, 1))
    assert repr(comp) == "(Zkouška)"

@pytest.mark.django_db
def test_internal_directives_repr():
    directive = InternalDirectives.objects.create(
        name="Bezpečnost", effective_date=date(2024, 5, 1)
    )
    assert repr(directive) == "(Bezpečnost)"

@pytest.mark.django_db
def test_cars_repr():
    car = Cars.objects.create(
        name="VW Golf", plate_number="ABC123", technical_inspection_date=date(2026, 1, 1)
    )
    assert repr(car) == "(VW Golf, ABC123)"

@pytest.mark.django_db
def test_real_estates_repr():
    real_estate = RealEstates.objects.create(
        name="Budova A", type="Budova", address="Adresa 1"
    )
    assert repr(real_estate) == "(Budova A)"

@pytest.mark.django_db
def test_employee_personal_competence_str():
    emp = Employee.objects.create(
        name="Jan", surname="Patočka", personal_number=886546,
        date_of_birth=date(1990, 1, 1), place_of_birth="Praha-Řeporyje", nationality="CZ",
        address="Křivonožská 9 & 3/4", email="jan.patocka@charta.cz",
        start_date_of_employment=date(2020, 1, 1),
        contract_from=date(2020, 1, 1), contract_until=date(2025, 1, 1)
    )
    comp = PersonalCompetence.objects.create(
        name="Cokoliv", valid_until=date(2030, 1, 1)
    )
    epc = EmployeePersonalCompetence.objects.create(
        employee=emp,
        competence=comp
    )
    assert str(epc) == f"{str(emp)} - {str(comp)}"

