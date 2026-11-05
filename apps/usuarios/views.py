from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


def iniciar_sesion(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('core:inicio')
    return render(request, 'usuarios/login.html', {'form': form})


def cerrar_sesion(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('core:inicio')


def registro(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        login(request, usuario)
        messages.success(request, 'Tu cuenta fue creada correctamente.')
        return redirect('core:inicio')
    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html')
