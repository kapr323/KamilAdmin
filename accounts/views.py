from django.contrib.auth import login, update_session_auth_hash
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


def home(request):
    return render(request, 'home.html')


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Pokud je to první přihlášení (uživatel musí změnit heslo), přesměruj na stránku pro změnu hesla
            if user.must_change_password:
                return redirect('change_password')  # Tady odkazujeme na URL pro změnu hesla
            return redirect('home')  # Po přihlášení uživatele přesměruj na domovskou stránku
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Udržuje autentifikaci uživatele po změně hesla
            request.user.must_change_password = False  # Nastavíme, že uživatel už nemusí měnit heslo
            request.user.save()
            return redirect('home')  # Po změně hesla přesměrujeme na domovskou stránku
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})