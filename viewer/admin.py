from django.contrib import admin
from django import forms
from django.forms.widgets import SelectDateWidget
from django.contrib.admin import ModelAdmin

from viewer.models import *


class KamilAdmin(ModelAdmin):
    @staticmethod
    def cleanup_description(modeladmin, request, queryset):
        queryset.update(description=None)

class EmployeeForm(forms.ModelForm):
        class Meta:
            model = Employee
            fields = '__all__'
            widgets = {
                'date_of_birth': SelectDateWidget(years=range(1900, 2050)),  # Rozsah let
                'start_date_of_employment': SelectDateWidget(years=range(1900, 2050)),
                'contract_from': SelectDateWidget(years=range(1900, 2050)),
                'contract_until': SelectDateWidget(years=range(1900, 2050)),
            }

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm
    # Register your models here.


@admin.register(EmployeePersonalCompetence)
class EmployeePersonalCompetenceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'competence', 'fulfilled')
    list_filter = ('competence',)
    search_fields = ('employee__name', 'employee__surname', 'competence__name')


@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade']
    filter_horizontal = ['personal_competencies']

admin.site.register(SalaryGrade)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(AgreementWorker)
admin.site.register(PersonalCompetence)
admin.site.register(InternalDirectives)
admin.site.register(Cars)
admin.site.register(RealEstates)