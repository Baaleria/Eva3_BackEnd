from django.shortcuts import render

from apps.catalogo.models import Producto


def inicio(request):
    destacados = Producto.objects.filter(
        activo=True, destacado=True
    )

    return render(request, 'core/index.html', {
        'destacados': destacados,
    })

def nosotros(request):
    return render(request, 'core/nosotros.html')