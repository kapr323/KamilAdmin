from enum import unique

from django.db import models
from django.db.models import Model, CharField, DateField
from django.forms import IntegerField


# Create your models here.
class JobPosition(Model):
    name = CharField(max_length=100, null=False, blank=False, unique=False)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class SalaryGrade(Model):
    grade = IntegerField(null=False, blank=False, unique=False)

    class Meta:
        ordering = ['grade']

    def __repr__(self):
        return self.grade

    def __str__(self):
        return self.grade


class Employee(Model):
    name = CharField(max_length=20, null=False, blank=False, unique=False)
    surname = CharField(max_length=32, null=False, blank=False, unique=False)
    title_before_name = CharField(max_length=20, null=True, blank=True, unique=False)
    title_after_name = CharField(max_length=20, null=True, blank=True, unique=False)
    personal_number = IntegerField(null=False, blank=True, unique=True)
    date_of_birth = DateField(null=False, blank=False, unique=False)
    place_of_birth = CharField(max_length=40, null=False, blank=False, unique=False)
    nationality = CharField(max_length=20, null=False, blank=False, unique=False)
    address = CharField(max_length=100, null=False, blank=False, unique=False)
    date_of_employment = DateField(null=False, blank=False, unique=False)
    creditable_work_experience = IntegerField(null=False, blank=False, default=0,
                                                  help_text="Délka praxe v měsících")
    education_level = CharField(max_length=20, null=False, blank=False, unique=False)
    type_of_employment = CharField(max_length=20, null=False, blank=False, unique=False)

    class Meta:
        ordering = ['surname', 'name']

    def __repr__(self):
        return f"({self.name, self.surname, self.personal_number})"

    def __str__(self):
        return f"{self.name} ({self.surname}) {self.personal_number}"


class Contract(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=False)
    contract_until = DateField(null=False, blank=False, unique=False)

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


