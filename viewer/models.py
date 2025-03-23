from datetime import timezone
from enum import unique

from django.db import models
from django.db.models import Model, CharField, DateField, IntegerField, ForeignKey, SET_NULL
from django.forms import BooleanField


# Create your models here.
class JobPosition(Model):
    name = CharField(max_length=100, null=False, blank=False, unique=False)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


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
    grade = IntegerField(null=False, blank=False, unique=False)
    step = IntegerField(null=False, blank=False, unique=False, default=1)

    class Meta:
        ordering = ['grade']

    def __repr__(self):
        return f"({self.grade, self.step})"

    def __str__(self):
        return f"{self.grade}-{self.step}"


class Contract(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=False)

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
    name = CharField(max_length=100, null=False, blank=False, unique=True)
    effective_date = DateField(null=False, blank=False, unique=False)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"({self.name})"

    def __str__(self):
        return self.name


class Cars(Model):
    name = CharField(max_length=100, null=False, blank=False, unique=False)
    type = CharField(max_length=50, null=False, blank=False, unique=False)
    plate_number = CharField(max_length=15, null=False, blank=False, unique=False)
    technical_inspection_date = DateField(null=False, blank=False, unique=False)
    highway_ticket_validity = DateField(null=False, blank=False, unique=False)
    is_usable = BooleanField()

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"({self.name}, {self.plate_number})"

    def __str__(self):
        return self.name


class RealEstates(Model):
    name = CharField(max_length=100, null=False, blank=False, unique=False)
    type = CharField(max_length=50, null=False, blank=False, unique=False)
    address = CharField(max_length=100, null=False, blank=False, unique=False)
    is_usable = BooleanField()

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"({self.name})"

    def __str__(self):
        return self.name
