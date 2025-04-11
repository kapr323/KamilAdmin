import re
from enum import unique

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model, CharField, DateField, IntegerField, ForeignKey, SET_NULL, BooleanField, TextChoices, \
    ManyToManyField, FileField
from django.core.validators import MinValueValidator, EmailValidator

from django.contrib.auth.models import User, Permission


# Funkce pro validaci telefonního čísla
def validate_phone_number(value):
    # Regex pro validaci telefonního čísla ve formátu +420 a 9 číslic
    if not re.match(r'^\+420\d{9}$', value):
        raise ValidationError('Telefonní číslo musí začínat +420 a následovat 9 číslic.')


class Employee(Model):
    class EducationLevel(TextChoices):
        SECONDARY_EDUCATION = 'Střední vzdělání s maturitou'
        BACHELOR_UNIVERSITY_DEGREE = 'Vysokoškolské vzdělání bakalářské'
        MASTER_UNIVERSITY_DEGREE = 'Magisterské vysokoškolské vzdělání'

    class TypeOfEmployment(TextChoices):
        MAIN_EMPLOYMENT_RELATIONSHIP = "Hlavní pracovní poměr"
        PART_TIME_JOB = 'Částečný pracovní úvazek'
        VACANT_REPRESENTATIVE = 'Uvolněný zastupitel'

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='employee')
    name = CharField(max_length=20, null=False, blank=False, unique=False)
    surname = CharField(max_length=32, null=False, blank=False, unique=False)
    title_before_name = CharField(max_length=20, null=True, blank=True, unique=False)
    title_after_name = CharField(max_length=20, null=True, blank=True, unique=False)
    personal_number = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Osobní číslo')
    job_position = ForeignKey('JobPosition', null=True, blank=True, on_delete=SET_NULL,
                              related_name='employee_job_position')
    date_of_birth = DateField(null=False, blank=False, unique=False)
    place_of_birth = CharField(max_length=40, null=False, blank=False, unique=False)
    nationality = CharField(max_length=20, null=False, blank=False, unique=False)
    address = CharField(max_length=100, null=False, blank=False, unique=False)
    email = models.EmailField(max_length=100, unique=True, blank=False, null=False, default='',
                              validators=[EmailValidator()])
    phone_number = models.CharField(
        max_length=13,  # Maximální délka pro +420 a 9 číslic
        blank=True,  # Telefonní číslo není povinné
        null=True,  # Telefonní číslo může být prázdné
        validators=[validate_phone_number]  # Přidání validace
    )
    start_date_of_employment = DateField(null=False, blank=False, unique=False)
    contract_from = DateField(null=False, blank=False, unique=False, default=None)
    contract_until = DateField(null=False, blank=False, unique=False, default=None)
    initial_creditable_work_experience_years = models.PositiveIntegerField(default=0)
    initial_creditable_work_experience_months = models.PositiveIntegerField(default=0,
                                                                            choices=[(i, str(i)) for i in range(12)])
    initial_creditable_work_experience_days = models.PositiveIntegerField(default=0,
                                                                          choices=[(i, str(i)) for i in range(31)])
    education_level = CharField(max_length=50, choices=EducationLevel.choices,
                                default=EducationLevel.SECONDARY_EDUCATION)
    type_of_employment = CharField(max_length=50, choices=TypeOfEmployment.choices,
                                   default=TypeOfEmployment.MAIN_EMPLOYMENT_RELATIONSHIP)
    image = models.ImageField(upload_to='employee_images/', null=True,
                              blank=True)  # Přidání obrázku


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


    # Použijeme stejný model jako pro Employee
class AgreementWorker(Model):  # Vytvoření podtřídy pro pracovníky s dohodami
    class TypeOfAgreement(TextChoices):
        WORK_AGREEMENT = 'Dohoda o pracovní činnosti'
        PERFORMANCE_WORK_AGREEMENT = 'Dohoda o provedení práce'

    id = models.AutoField(primary_key=True)

    # Nastavíme propojení mezi AgreementWorker a Employee, ale ne dědění
    employee = models.OneToOneField('Employee', on_delete=models.CASCADE)

    # Povinné pole pro jméno a příjmení
    name = CharField(max_length=20, null=False, blank=False)
    surname = CharField(max_length=32, null=False, blank=False)

    # Titul před a po jménu
    title_before_name = CharField(max_length=20, null=True, blank=True)
    title_after_name = CharField(max_length=20, null=True, blank=True)

    # Osobní údaje
    date_of_birth = DateField(null=False, blank=False)
    place_of_birth = CharField(max_length=40, null=False, blank=False)
    address = CharField(max_length=100, null=True, blank=True)

    # Kontaktní informace
    email = models.EmailField(max_length=100, null=True, blank=True, default='', validators=[EmailValidator()])
    phone_number = models.CharField(max_length=13, blank=True, null=True, validators=[validate_phone_number])

    # Typ dohody a platnost
    type_of_agreement = CharField(max_length=32, choices=TypeOfAgreement.choices,
                                    default=TypeOfAgreement.PERFORMANCE_WORK_AGREEMENT)
    contract_from = DateField(null=False, blank=False)
    contract_until = DateField(null=False, blank=False)

    # Hodinová mzda
    hourly_wage = models.DecimalField(null=True, max_digits=5, decimal_places=0)

    class Meta:
        verbose_name = "Pracovník s dohodou"
        verbose_name_plural = "Pracovníci s dohodami"

    def save(self, *args, **kwargs):
        if self.type_of_agreement not in [self.TypeOfAgreement.WORK_AGREEMENT, self.TypeOfAgreement.PERFORMANCE_WORK_AGREEMENT]:
            raise ValidationError(
                "Pracovník musí mít typ pracovního poměru 'Dohoda o pracovní činnosti' nebo 'Dohoda o provedení práce'."
            )
        super().save(*args, **kwargs)

    def __repr__(self):
        return f"({self.name} {self.surname})"

    def __str__(self):
        return f"{self.name} {self.surname}"


class PersonalCompetence(Model):
    name = CharField(max_length=50)
    valid_until = DateField()
    job_position = models.ForeignKey('JobPosition', on_delete=models.CASCADE, related_name='competencies', null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"({self.name})"

    def __str__(self):
        return self.name


class EmployeePersonalCompetence(Model):
    employee = ForeignKey('Employee', on_delete=models.CASCADE)
    competence = ForeignKey('PersonalCompetence', on_delete=models.CASCADE)
    certificate = FileField(upload_to='certificates/', blank=True, null=True)
    valid_until = DateField(null=True, blank=True)  # Platnost certifikátu

    class Meta:
        ordering = ['competence']

    @property
    def fulfilled(self):
        return bool(self.certificate)

    def __str__(self):
        return f"{self.employee} – {self.competence}"


# Create your models here.
class JobPosition(Model):
    name = CharField(max_length=100)
    grade = IntegerField(default=8)
    personal_competencies = ManyToManyField('PersonalCompetence', related_name='job_positions')
    permissions = models.ManyToManyField(Permission, blank=True,
                                         related_name='job_positions')

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class InternalDirectives(Model):
    class InternalDirectiveChoices(TextChoices):
        REGULATIONS = 'Řád'
        DIRECTIVES = 'Směrnice'
        RULES = 'Nařízení'

    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    effective_date = models.DateField(null=False, blank=False)
    document = models.FileField(upload_to='internal_documents/', blank=True, null=True)  # Přidání pole pro nahrání PDF
    description = models.TextField(blank=True, null=True)  # Popis dokumentu

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
    highway_ticket_validity = DateField(null=True, blank=True, unique=False)
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


class RolePermissions(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('secretary', 'Tajemník'),
        ('mayor', 'Starosta'),
        ('department_head', 'Vedoucí odboru'),
        ('employee', 'Zaměstnanec'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    model_name = models.CharField(max_length=100)
    field_name = models.CharField(max_length=100)
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.role} - {self.model_name} - {self.field_name}"