from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.catalogo.models import Categoria, Producto


class Command(BaseCommand):
    help = "Carga datos de prueba para Valeria's Vanity"

    def handle(self, *args, **options):
        # 1. Categorías
        categorias = {}
        datos_categorias = [
            ('Skincare', 'Cuidado facial: limpieza, hidratación y tratamiento.'),
            ('Cabello', 'Shampoos, mascarillas y tratamientos capilares.'),
            ('Maquillaje', 'Labiales, bases, sombras y más.'),
            ('Cuerpo', 'Cremas, exfoliantes y cuidado corporal.'),
        ]
        for nombre, descripcion in datos_categorias:
            cat, _ = Categoria.objects.get_or_create(
                nombre=nombre, defaults={'descripcion': descripcion})
            categorias[nombre] = cat

        # 2. Productos
        productos = [
            # codigo, nombre, marca, contenido, categoria, precio, stock, destacado
            ('SKN-001', 'Crema Hidratante Facial', 'CeraVe', '50 ml', 'Skincare', 14990, 25, True),
            ('SKN-002', 'Sérum Vitamina C', 'The Ordinary', '30 ml', 'Skincare', 12990, 18, False),
            ('CAB-001', 'Shampoo Reparador', 'Pantene', '400 ml', 'Cabello', 5990, 40, False),
            ('CAB-002', 'Mascarilla Capilar Nutritiva', 'Kérastase', '200 ml', 'Cabello', 22990, 10, True),
            ('MAQ-001', 'Labial Mate Rojo', 'Maybelline', '4 g', 'Maquillaje', 6990, 30, True),
            ('MAQ-002', 'Base Líquida Cobertura Media', "L'Oréal", '30 ml', 'Maquillaje', 11990, 20, False),
            ('CUE-001', 'Crema Corporal Hidratante', 'Nivea', '250 ml', 'Cuerpo', 4990, 35, False),
            ('CUE-002', 'Exfoliante Corporal de Coco', 'Dove', '225 g', 'Cuerpo', 7490, 0, False),
        ]
        for codigo, nombre, marca, contenido, cat, precio, stock, destacado in productos:
            Producto.objects.get_or_create(
                codigo=codigo,
                defaults={
                    'nombre': nombre,
                    'marca': marca,
                    'contenido': contenido,
                    'categoria': categorias[cat],
                    'descripcion': f'{nombre} de {marca}, ideal para tu rutina diaria.',
                    'precio': precio,
                    'stock': stock,
                    'estado': 'DISP' if stock > 0 else 'AGOT',
                    'destacado': destacado,
                },
            )

        # 3. Usuarios de prueba
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin', 'admin@valeriasvanity.cl', 'Admin12345!')
        if not User.objects.filter(username='cliente').exists():
            User.objects.create_user(
                'cliente', 'cliente@valeriasvanity.cl', 'Cliente12345!',
                first_name='Clienta', last_name='Demo')

        self.stdout.write(self.style.SUCCESS('Datos cargados correctamente.'))