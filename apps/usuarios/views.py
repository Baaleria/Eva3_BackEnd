from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LoginForm, RegistroForm


def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect('catalogo:lista')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"¡Bienvenida/o {user.first_name}! Tu cuenta fue creada.")
            return redirect('catalogo:lista')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('catalogo:lista')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Sesión iniciada correctamente.")
            siguiente = request.POST.get('next', '')
            if siguiente and url_has_allowed_host_and_scheme(
                    siguiente, allowed_hosts={request.get_host()}):
                return redirect(siguiente)
            return redirect('catalogo:lista')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {
        'form': form,
        'next': request.GET.get('next', ''),
    })


def cerrar_sesion(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, "Has cerrado sesión.")
    return redirect('core:inicio')


@login_required
def perfil_usuario(request):
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})
