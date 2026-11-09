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
            categoria, _ = Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': descripcion},
            )
            categorias[nombre] = categoria

        productos = [
            # codigo, nombre, marca, contenido, categoria, precio, stock, destacado
            ('CAB-001','Gel para el cabello Fijación Alta', 'Etniker', '1000ml', 'Cabello', 34990, 10, False),
            ('CAB-002','Shampoo para cabello rizado', "L'OREAL", '300ml', 'Cabello', 27621, 10, False),
            ('MAQ-001','Rubor Barra Blushin Charm', 'Catrice', '5.5g', 'Maquillaje', 5990, 10, True),
            ('MAQ-002','Mascara de pestañas voluminizadora','L´OREAL','9.9ml', 'Maquillaje',15390,3,False),
            ('SKN-001','Serum Protector Solar Madagascar Centella Hyalu-Cica Water-Fit Sun Serum (SPF50+ PA++++) ', 'SKIN1004', '50ml', 'Skincare', 13383,5, True),
            ('SKN-002', 'Madagascar Centella Poremizing Quick Clay Stick Mask', 'SKIN1004', '27g', 'Skincare',28900, 10,False),
            ('CUE-001','Loción coporal Coco & Aceite de Monoi','NIVEA','400ml','Cuerpo',8599,10, True),
            ('CUE-002', 'Dove Tono Uniforme', 'Dove', '45g', 'Cuerpo', 1690,10,False),
        ]

        for codigo, nombre, marca, contenido, categoria, precio, stock, destacado in productos:
            Producto.objects.update_or_create(
                codigo=codigo,
                defaults={
                    'nombre': nombre,
                    'marca': marca,
                    'contenido': contenido,
                    'categoria': categorias[categoria],
                    'descripcion': f'{nombre} de {marca}',
                    'precio': precio,
                    'stock': stock,
                    'estado': 'DISP' if stock > 0 else 'AGOT',
                    'destacado': destacado,
                },
            )

        self.stdout.write(self.style.SUCCESS('Datos cargados correctamente.'))
