from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductoForm
from .models import Producto


def lista(request):
    productos = Producto.objects.filter(activo=True).select_related('categoria')
    return render(request, 'catalogo/lista.html', {'productos': productos})


def detalle(request, slug):
    producto = get_object_or_404(
        Producto.objects.select_related('categoria'), slug=slug, activo=True
    )
    return render(request, 'catalogo/detalle.html', {'producto': producto})


@staff_member_required
def gestion(request):
    productos = Producto.objects.select_related('categoria')
    return render(request, 'catalogo/gestion.html', {'productos': productos})


@staff_member_required
def crear(request):
    form = ProductoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto creado correctamente.')
        return redirect('catalogo:gestion')
    return render(request, 'catalogo/crear.html', {'form': form})
