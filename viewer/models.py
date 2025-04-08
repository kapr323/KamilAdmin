from enum import unique

from django.db import models
from django.db.models import Model, CharField, DateField, IntegerField, ForeignKey, SET_NULL, BooleanField, TextChoices
from django.core.validators import MinValueValidator, EmailValidator


# Create your models here.
class JobPosition(Model):
    name = CharField(max_length=100, null=False, blank=False, unique=False)
    grade = IntegerField(default=8)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Employee(Model):
    class EducationLevel(TextChoices):
        SECONDARY_EDUCATION = 'Střední vzdělání s maturitou'
        BACHELOR_UNIVERSITY_DEGREE = 'Vysokoškolské vzdělání bakalářské'
        MASTER_UNIVERSITY_DEGREE = 'Magisterské vysokoškolské vzdělání'

    class TypeOfEmployment(TextChoices):
        MAIN_EMPLOYMENT_RELATIONSHIP = "Hlavní pracovní poměr"
        WORK_AGREEMENT = 'Dohoda o pracovní činnosti'
        PERFORMANCE_WORK_AGREEMENT = 'Dohoda o provedení práce'
        PART_TIME_JOB = 'Částečný pracovní úvazek'

    name = CharField(max_length=20, null=False, blank=False, unique=False)
    surname = CharField(max_length=32, null=False, blank=False, unique=False)
    title_before_name = CharField(max_length=20, null=True, blank=True, unique=False)
    title_after_name = CharField(max_length=20, null=True, blank=True, unique=False)
    personal_number = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Osobní číslo')
    job_position = ForeignKey("JobPosition", null=True, blank=False, unique=False, on_delete=SET_NULL, related_name='employee_job_position')
    date_of_birth = DateField(null=False, blank=False, unique=False)
    place_of_birth = CharField(max_length=40, null=False, blank=False, unique=False)
    nationality = CharField(max_length=20, null=False, blank=False, unique=False)
    address = CharField(max_length=100, null=False, blank=False, unique=False)
    email = models.EmailField(max_length=100, unique=False, blank=False, null=False, default='', validators=[EmailValidator()])
    start_date_of_employment = DateField(null=False, blank=False, unique=False)
    contract_from = DateField(null=False, blank=False, unique=False, default=None)
    contract_until = DateField(null=False, blank=False, unique=False, default=None)
    initial_creditable_work_experience_years = models.PositiveIntegerField(default=0)
    initial_creditable_work_experience_months = models.PositiveIntegerField(default=0,
                                                                            choices=[(i, str(i)) for i in range(12)])
    initial_creditable_work_experience_days = models.PositiveIntegerField(default=0,
                                                                          choices=[(i, str(i)) for i in range(31)])
    education_level = CharField(max_length=50, choices=EducationLevel.choices, default=EducationLevel.SECONDARY_EDUCATION)
    type_of_employment = CharField(max_length=50, choices=TypeOfEmployment.choices, default=TypeOfEmployment.MAIN_EMPLOYMENT_RELATIONSHIP)

    def total_initial_creditable_work_experience_in_days(self):
        return (self.initial_creditable_work_experience_years * 365 +
                self.initial_creditable_work_experience_months * 30 +
                self.initial_creditable_work_experience_days)

    class Meta:
        ordering = ['surname', 'name']

    def __repr__(self):
        return f"({self.name, self.surname, self.personal_number})"

    def __str__(self):
        return f"{self.name} ({self.surname}) {self.personal_number}"


class SalaryGrade(Model):
    class SalaryGradeChoices(TextChoices):
        grade8 = '8. platová třída'
        grade9 = '9. platová třída'
        grade10 = '10. platová třída'
        grade11 = '11. platová třída'
        grade12 = '12. platová třída'

    class SalaryStepChoices(TextChoices):
        step1 = '1. platový stupeň'
        step2 = '2. platový stupeň'
        step3 = '3. platový stupeň'
        step4 = '4. platový stupeň'
        step5 = '5. platový stupeň'
        step6 = '6. platový stupeň'
        step7 = '7. platový stupeň'
        step8 = '8. platový stupeň'
        step9 = '9. platový stupeň'
        step10 = '10. platový stupeň'
        step11 = '11. platový stupeň'
        step12 = '12. platový stupeň'

    grade = IntegerField(default=8)
    step = IntegerField(default=1)

    class Meta:
        ordering = ['grade']

    def __repr__(self):
        return f"({self.grade, self.step})"

    def __str__(self):
        return f"{self.grade}-{self.step}"


class Contract(Model):
    class ContractChoices(TextChoices):
        MAIN_EMPLOYMENT_RELATIONSHIP = "Hlavní pracovní poměr"
        WORK_AGREEMENT = 'Dohoda o pracovní činnosti'
        PERFORMANCE_WORK_AGREEMENT = 'Dohoda o provedení práce'
        PART_TIME_JOB = 'Částečný pracovní úvazek'


    name = CharField(max_length=32, choices=ContractChoices.choices, default=ContractChoices.MAIN_EMPLOYMENT_RELATIONSHIP)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"({self.name})"

    def __str__(self):
        return self.name


class PersonalCompetence(Model):
    name = CharField(max_length=50, null=False, blank=False, unique=False)
    valid_until = DateField(null=False, blank=False, unique=False)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"({self.name})"

    def __str__(self):
        return self.name


class InternalDirectives(Model):
    class InternalDirectiveChoices(TextChoices):
        REGULATIONS =  'Řád'
        DIRECTIVES = 'Směrnice'
        RULES = 'Nařízení'

    type = CharField(max_length=50, choices=InternalDirectiveChoices.choices,
                     default=InternalDirectiveChoices.REGULATIONS)
    name = CharField(max_length=100, null=False, blank=False, unique=True)
    effective_date = DateField(null=False, blank=False, unique=False)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"({self.name})"

    def __str__(self):
        return self.name


class Cars(Model):
    class CarType(TextChoices):
        PASSENGER_VEHICLE = 'Osobní vozidlo'
        TRUCK = 'Nákladní vozidlo'

    class FuelType(TextChoices):
        DIESEL = 'Nafta'
        GASOLINE = 'Benzín'
        ELECTRIC = 'Elektrický pohon'
        LPG = 'LPG'

    name = CharField(max_length=100, null=False, blank=False, unique=False)
    type = CharField(max_length=50, choices=CarType.choices, default=CarType.PASSENGER_VEHICLE)
    plate_number = CharField(max_length=15, null=False, blank=False, unique=False)
    fuel_type = CharField(max_length=20, choices=FuelType.choices, default=FuelType.ELECTRIC)
    technical_inspection_date = DateField(null=False, blank=False, unique=False)
    highway_ticket_validity = DateField(null=False, blank=False, unique=False)
    is_usable = BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"({self.name}, {self.plate_number})"

    def __str__(self):
        return self.name


class RealEstates(Model):
    class RealEstatesType(TextChoices):
        BUILDING = 'Budova'
        RENTAL_APARTMENT = 'Nájemní byt'
        SOCIAL_HALL = 'Společenská místnost'
        CONFERENCE_ROOM = 'Zasedací místnost'

    name = CharField(max_length=100, null=False, blank=False, unique=False)
    type = CharField(max_length=50, choices=RealEstatesType.choices, default=RealEstatesType.CONFERENCE_ROOM)
    address = CharField(max_length=100, null=False, blank=False, unique=False)
    is_usable = BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"({self.name})"

    def __str__(self):
        return self.name
