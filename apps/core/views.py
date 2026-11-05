from django.shortcuts import render

from apps.catalogo.models import Categoria, Producto


def inicio(request):
    destacados = Producto.objects.filter(
        activo=True, destacado=True
    ).select_related('categoria')[:4]

    categorias = Categoria.objects.filter(activo=True)[:6]

    return render(request, 'core/index.html', {
        'destacados': destacados,
        'categorias': categorias,
    })


def nosotros(request):
    return render(request, 'core/nosotros.html')