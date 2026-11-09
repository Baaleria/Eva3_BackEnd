from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.catalogo.models import Producto


def _obtener_carrito(request):
    return request.session.setdefault('carrito', {})


def _calcular_totales(carrito):
    subtotal = sum(item['subtotal'] for item in carrito.values())
    iva = subtotal * 19 // 100
    total = subtotal + iva
    return subtotal, iva, total


def ver(request):
    carrito = _obtener_carrito(request)
    subtotal, iva, total = _calcular_totales(carrito)

    return render(request, 'pedidos/ver.html', {
        'items_carrito': carrito.values(),
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
        'esta_vacio': not carrito,
    })


@require_POST
def agregar(request, id):
    producto = get_object_or_404(Producto, id=id, activo=True)
    carrito = _obtener_carrito(request)
    str_id = str(producto.id)

    cantidad_actual = carrito.get(str_id, {}).get('cantidad', 0)
    nueva_cantidad = cantidad_actual + 1

    if nueva_cantidad > producto.stock:
        messages.warning(
            request,
            f"Stock disponible: {producto.stock} unidades "
            f"para '{producto.nombre}'.",
        )
        return redirect('pedidos:ver')

    precio = int(producto.precio)

    carrito[str_id] = {
        'id': producto.id,
        'nombre': producto.nombre,
        'slug': producto.slug,
        'marca': producto.marca,
        'precio': precio,
        'cantidad': nueva_cantidad,
        'subtotal': precio * nueva_cantidad,
        'imagen_url': producto.imagen.url if producto.imagen else '',
    }

    request.session.modified = True
    messages.success(request, f"'{producto.nombre}' añadido al carrito.")
    return redirect('pedidos:ver')


@require_POST
def restar(request, id):
    carrito = _obtener_carrito(request)
    str_id = str(id)

    if str_id in carrito:
        carrito[str_id]['cantidad'] -= 1

        if carrito[str_id]['cantidad'] <= 0:
            del carrito[str_id]
        else:
            carrito[str_id]['subtotal'] = (
                carrito[str_id]['precio'] * carrito[str_id]['cantidad']
            )

        request.session.modified = True

    return redirect('pedidos:ver')


@require_POST
def eliminar(request, id):
    carrito = _obtener_carrito(request)
    str_id = str(id)

    if str_id in carrito:
        del carrito[str_id]
        request.session.modified = True
        messages.info(request, 'Producto eliminado del carrito.')

    return redirect('pedidos:ver')


@require_POST
def limpiar(request):
    request.session.pop('carrito', None)
    return redirect('pedidos:ver')


@login_required
@require_POST
def checkout_simulado(request):
    carrito = _obtener_carrito(request)

    if not carrito:
        messages.info(request, 'Tu carrito está vacío.')
        return redirect('pedidos:ver')

    # Comprobar nuevamente el stock antes de confirmar.
    for item in carrito.values():
        producto = Producto.objects.filter(
            id=item['id'],
            activo=True,
        ).first()

        if producto is None or item['cantidad'] > producto.stock:
            messages.warning(
                request,
                f"No hay stock suficiente para '{item['nombre']}'. "
                "Revisa tu carrito.",
            )
            return redirect('pedidos:ver')

    subtotal, iva, total = _calcular_totales(carrito)
    items_comprados = list(carrito.values())

    del request.session['carrito']

    return render(request, 'pedidos/conf_pedido.html', {
        'items': items_comprados,
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
        'orden_id': f'VV-{request.user.id}-2026',
    })
