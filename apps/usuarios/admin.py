from django.contrib import admin

from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rut', 'telefono', 'rol')
    search_fields = ('usuario__username', 'rut', 'telefono')
    list_filter = ('rol',)
    readonly_fields = ('rol',)