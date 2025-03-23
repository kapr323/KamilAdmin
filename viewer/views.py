from django.shortcuts import render

from viewer.models import *


def home(request):
    return render(request, 'home.html')


def employees(request):
    employees_ = Employee.objects.all()
    context = {'employees': employees_}
    return render(request=request,
                  template_name="employees.html",
                  context=context)