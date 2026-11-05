from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.catalogo.models import Categoria, Producto


class Command(BaseCommand):
    help = "Carga datos de prueba para Valeria's Vanity"

    @transaction.atomic
    def handle(self, *args, **options):
        datos_categorias = [
            ('Skincare', 'Cuidado facial: limpieza, hidratación y tratamiento.'),
            ('Cabello', 'Shampoos, mascarillas y tratamientos capilares.'),
            ('Maquillaje', 'Labiales, bases, sombras y más.'),
            ('Cuerpo', 'Cremas, exfoliantes y cuidado corporal.'),
        ]
        categorias = {}
        for nombre, descripcion in datos_categorias:
            categoria, _ = Categoria.objects.update_or_create(
                nombre=nombre,
                defaults={'descripcion': descripcion},
            )
            categorias[nombre] = categoria

        productos = [
            # codigo, nombre, marca, contenido, categoria, precio, stock, destacado
            ('CAB-001', 'Gel para el cabello Fijación Alta', 'Etniker', 'Gel espeso', 'Cabello', 34990, 10, False),
            ('CAB-002', 'Shampoo para cabello rizado', "L'OREAL", 'Shampoo con glicerina', 'Cabello', 27621, 10, False),
            ('MAQ-001', 'Rubor Barra Blushin Charm', 'Catrice', 'Rubor tono tostado', 'Maquillaje', 5990, 10, False),
        ]

        for codigo, nombre, marca, contenido, categoria, precio, stock, destacado in productos:
            Producto.objects.update_or_create(
                codigo=codigo,
                defaults={
                    'nombre': nombre,
                    'marca': marca,
                    'contenido': contenido,
                    'categoria': categorias[categoria],
                    'descripcion': f'{nombre} de {marca}, ideal para tu rutina diaria.',
                    'precio': precio,
                    'stock': stock,
                    'estado': 'DISP' if stock > 0 else 'AGOT',
                    'destacado': destacado,
                },
            )

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin', 'admin@valeriasvanity.cl', 'Admin12345!')
        if not User.objects.filter(username='cliente').exists():
            User.objects.create_user(
                'cliente', 'cliente@valeriasvanity.cl', 'Cliente12345!',
                first_name='Clienta', last_name='Demo')

        self.stdout.write(self.style.SUCCESS('Datos cargados correctamente.'))
