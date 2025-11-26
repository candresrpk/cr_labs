from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('web:home')
            else:
                messages.error(request, "Error en el inicio de sesión. Por favor, verifica tus credenciales.")
        else:
            messages.error(request, "Error en el inicio de sesión. Por favor, verifica tus credenciales.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('web:home')


@transaction.atomic
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, "Registro exitoso. ¡Bienvenido!")
                return redirect('web:home')
            except Exception as e:
                messages.error(request, f"Error al crear el perfil: {e}")
        else:
            messages.error(request, "Error en el registro. Por favor, verifica los campos.")
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})



@login_required
def profile_view(request):
    
    username = request.user.username
    
    context = {'username': username}
    return render(request, 'accounts/profile.html', context)