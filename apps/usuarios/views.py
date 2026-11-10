from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.db import transaction

from .forms import LoginForm, RegistroForm
from .models import Perfil


def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect('catalogo:lista')

    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = form.save()

                Perfil.objects.create(
                    usuario=user,
                    rut=form.cleaned_data['rut'],
                    telefono=form.cleaned_data['telefono'],
                    rol=Perfil.Rol.CLIENTE,
                )

            login(request, user)
            messages.success(
                request,
                f"¡Bienvenida/o {user.first_name}! Tu cuenta fue creada.",
            )
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
    rol = (
        Perfil.Rol.PERSONAL
        if request.user.is_staff or request.user.is_superuser
        else Perfil.Rol.CLIENTE
    )

    perfil, _ = Perfil.objects.get_or_create(
        usuario=request.user,
        defaults={'rol': rol},
    )

    if perfil.rol != rol:
        perfil.rol = rol
        perfil.save(update_fields=['rol'])

    return render(request, 'usuarios/perfil.html', {
        'usuario': request.user,
        'perfil': perfil,
    })
