from django.conf import settings
from django.db import models


class Perfil(models.Model):
    class Rol(models.TextChoices):
        CLIENTE = 'CLIENTE', 'Cliente'
        PERSONAL = 'PERSONAL', 'Personal de tienda'

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil',
    )
    rut = models.CharField(max_length=12, blank=True, verbose_name='RUT')
    telefono = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono',
    )
    rol = models.CharField(
        max_length=10,
        choices=Rol.choices,
        default=Rol.CLIENTE,
    )

    def __str__(self):
        return f'Perfil de {self.usuario.username}'
