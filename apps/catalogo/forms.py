from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo', 'nombre', 'categoria', 'marca', 'contenido', 'descripcion',
            'precio', 'stock', 'estado', 'imagen', 'destacado', 'activo',
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. SKN-003'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Crema Hidratante Facial'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. CeraVe'}),
            'contenido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 50 ml'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo', '').strip().upper()
        existe = Producto.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists()
        if existe:
            raise forms.ValidationError("Ya existe un producto con este código.")
        return codigo

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio debe ser superior a 0 CLP.")
        return precio