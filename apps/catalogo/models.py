from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Producto(models.Model):
    class Estado(models.TextChoices):
        DISPONIBLE = 'DISP', 'Disponible'
        AGOTADO = 'AGOT', 'Agotado'
        DESCONTINUADO = 'DESC', 'Descontinuado'

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
    )
    codigo = models.CharField('Código SKU', max_length=20, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    nombre = models.CharField(max_length=200)
    marca = models.CharField(max_length=100)
    contenido = models.CharField(max_length=50, blank=True, help_text="Ej: 50 ml")
    descripcion = models.TextField()
    precio = models.DecimalField(
        max_digits=10, decimal_places=0,
        validators=[MinValueValidator(0)],
    )
    stock = models.PositiveIntegerField(default=0)
    estado = models.CharField(
        max_length=4,
        choices=Estado.choices,
        default=Estado.DISPONIBLE,
    )
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    destacado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} ({self.marca})"

    @property
    def en_stock(self):
        return self.stock > 0

    @property
    def precio_formateado(self):
        return f"${self.precio:,.0f}".replace(",", ".")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.nombre}-{self.codigo}")
        super().save(*args, **kwargs)