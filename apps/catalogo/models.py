from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Categoría")
    slug = models.SlugField(max_length=120, unique=True, blank=True, help_text="URL amigable")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    activo = models.BooleanField(default=True, verbose_name="¿Activo?")
    creado_en = models.DateTimeField(auto_now_add=True)

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

    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código SKU")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT,
        related_name="productos", verbose_name="Categoría",
    )
    marca = models.CharField(max_length=100, verbose_name="Marca")
    contenido = models.CharField(max_length=50, blank=True, verbose_name="Contenido (ml / g)")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(
        max_digits=10, decimal_places=0,
        validators=[MinValueValidator(0)], verbose_name="Precio en CLP",
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock disponible")
    estado = models.CharField(
        max_length=4, choices=Estado.choices,
        default=Estado.DISPONIBLE, verbose_name="Estado",
    )
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True, verbose_name="Fotografía")
    destacado = models.BooleanField(default=False, verbose_name="¿Destacado?")
    activo = models.BooleanField(default=True, verbose_name="¿Disponible?")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Productos Cosméticos"
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
            base_slug = slugify(self.nombre)
            slug = base_slug
            contador = 1
            while Producto.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug
        super().save(*args, **kwargs)
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