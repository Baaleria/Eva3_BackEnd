from django.contrib import admin
from .models import Categoria, Producto

admin.site.site_header = "Valeria's Vanity - Panel de Control"
admin.site.site_title = "Valeria's Vanity Admin"
admin.site.index_title = "Gestión Operativa de Productos y Pedidos"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'activo', 'creado_en')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}
    list_editable = ('activo',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'marca', 'precio_formateado',
                    'stock', 'estado', 'activo', 'destacado')
    list_filter = ('categoria', 'estado', 'marca', 'activo', 'destacado')
    search_fields = ('codigo', 'nombre', 'marca', 'descripcion')
    list_editable = ('stock', 'estado', 'activo', 'destacado')
    prepopulated_fields = {'slug': ('nombre',)}
    list_select_related = ('categoria',)
    list_per_page = 15
    fieldsets = (
        ('Identificación', {
            'fields': ('codigo', 'nombre', 'slug', 'categoria', 'marca'),
        }),
        ('Detalle y multimedia', {
            'fields': ('contenido', 'descripcion', 'imagen'),
        }),
        ('Precio e inventario', {
            'fields': ('precio', 'stock', 'estado'),
        }),
        ('Visibilidad', {
            'fields': ('destacado', 'activo'),
        }),
    )