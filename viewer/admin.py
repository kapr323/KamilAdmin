from django.contrib import admin
from django.contrib.admin import ModelAdmin

from viewer.models import *


class KamilAdmin(ModelAdmin):
    @staticmethod
    def cleanup_description(modeladmin, request, queryset):
        queryset.update(description=None)
    # Register your models here.

admin.site.register(JobPosition)
admin.site.register(SalaryGrade)
admin.site.register(Employee)
admin.site.register(Contract)
admin.site.register(PersonalCompetence)
admin.site.register(InternalDirectives)
admin.site.register(Cars)
admin.site.register(RealEstates)