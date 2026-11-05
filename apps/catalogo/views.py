from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductoForm
from .models import Categoria, Producto


def lista(request):
    query = request.GET.get('q', '').strip()
    categoria_slug = request.GET.get('categoria', '')
    orden = request.GET.get('orden', 'recientes')

    productos = Producto.objects.filter(activo=True).select_related('categoria')

    if categoria_slug:
        productos = productos.filter(categoria__slug=categoria_slug)

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) |
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(marca__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )

    ordenes_validos = {
        'precio_asc': 'precio',
        'precio_desc': '-precio',
        'nombre_asc': 'nombre',
        'recientes': '-fecha_creacion',
    }
    productos = productos.order_by(ordenes_validos.get(orden, '-fecha_creacion'))

    paginador = Paginator(productos, 6)
    pagina = paginador.get_page(request.GET.get('page'))
    categorias = Categoria.objects.filter(activo=True)

    return render(request, 'catalogo/lista.html', {
        'productos': pagina,
        'categorias': categorias,
        'categoria_seleccionada': categoria_slug,
        'query_actual': query,
        'orden_actual': orden,
        'total_resultados': productos.count(),
    })


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
