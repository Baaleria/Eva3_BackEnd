from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
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


def es_administrador(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def gestion(request):
    productos = Producto.objects.select_related('categoria').order_by('categoria__nombre', 'nombre')
    return render(request, 'catalogo/gestion.html', {'productos': productos})


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def crear(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado correctamente.')
            return redirect('catalogo:gestion')
    else:
        form = ProductoForm()
    return render(request, 'catalogo/producto.html', {
        'form': form,
        'titulo': 'Nuevo producto',
    })


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def editar(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        form = ProductoForm(
            request.POST,
            request.FILES,
            instance=producto,
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"Producto '{producto.nombre}' actualizado.",
            )
            return redirect('catalogo:gestion')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'catalogo/producto.html', {
        'form': form,
        'producto': producto,
        'titulo': 'Editar Producto',
        'boton_texto': 'Actualizar',
    })


@login_required
@user_passes_test(es_administrador, login_url='catalogo:lista')
def eliminar(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado.')
        return redirect('catalogo:gestion')

    return render(
        request,
        'catalogo/conf_eliminar.html',
        {'producto': producto},
    )