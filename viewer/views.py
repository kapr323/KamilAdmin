from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def user_account(request):
    return render(request, 'user_account.html')

def user_settings(request):
    return render(request, 'user_settings.html')

def user_favorite(request):
    return render(request, 'user_favorite.html')

def reservation_system(request):
    return render(request, 'reservation_system.html')