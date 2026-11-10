# Eva3_BackEnd
## Ficha de registro de la propuesta
 
| Campo | Detalle |
|---|---|
| **Nombre de la Organización o Plataforma** | Valeria's Vanity |
| **Modelo de Negocio / Giro** | Tienda de cosméticos (skincare, cabello, maquillaje y cuidado de la piel) |
| **Integrantes del Equipo** | Andrea Lara – 28242134-8  |
| **Entidad de Contexto / Agrupación (ORM)** | `Categoria` (Skincare, Cabello, Maquillaje, Cuerpo) |
| **Entidad Principal Gestionable (ORM)** | `Producto` (productos cosméticos) |
| **Propósito de la Sesión (`request.session`)** | Carrito de compras: el usuario agrega productos, modifica cantidades y ve subtotal, IVA (19%) y total antes de confirmar |


 ## Instalación paso a paso
 
**1. Clonar el repositorio**
 
```bash
git clone https://github.com/Baaleria/Eva3_BackEnd.git
cd Eva3_BackEnd
```
 
**2. Crear y activar el entorno virtual**
 
Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```
 
macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
 
**3. Instalar las dependencias**
 
```bash
pip install -r requirements.txt
```
 
**4. Crear la base de datos**
 
```bash
python manage.py migrate
```
 
**5. Cargar los datos de prueba**
 
```bash
python manage.py poblar_datos
```
 
Este comando crea 4 categorías, 8 productos y los usuarios de prueba (`admin` y `cliente`).
 
**6. Iniciar el servidor**
 
```bash
python manage.py runserver
```
 
Abrir en el navegador: http://127.0.0.1:8000/
 
---
 
## Credenciales de prueba
 
| Rol | Usuario | Contraseña | Acceso |
|---|---|---|---|
| Administrador (staff) | `admin` | `Admin12345!` | Sitio, inventario y Django Admin |
| Cliente | `cliente` | `Cliente12345!` | Catálogo, carrito y compra |
 
También se puede crear una cuenta nueva desde **Registro**, que queda con rol Cliente.
 
---

## Bitácora de uso de Inteligencia Artificial

**Herramienta utilizada:** Claude (Anthropic)

### Caso 1: Validación del código único del producto (ORM)

| Caso 1 | Validación del código único del producto |
|---|---|
| **Prompt** | Estoy haciendo una tienda de cosméticos en Django. Mi modelo `Producto` tiene un campo `codigo` con `unique=True` y quiero validarlo en el `ModelForm` con un `clean_codigo`, para que si lo repiten salga un mensaje en el formulario y no un error de la base de datos. El problema es que al editar un producto me dice que el código ya existe, ¿cómo lo soluciono? |
| **Respuesta técnica** | Propuso un método `clean_codigo` en `ProductoForm` que limpia el valor, busca otro producto con ese código y lanza `ValidationError` si existe. Explicó que hay que excluir el propio registro con `exclude(pk=self.instance.pk)`: al crear, `instance.pk` es `None` y no excluye nada, y al editar excluye el producto actual para que no choque consigo mismo. |
| **Adaptación aplicada** | La guía del profesor solo valida el precio (`clean_precio`), así que la mantuve y agregué la validación del código, porque la pauta exige un identificador único validado. Pasé el código a mayúsculas para que `skn-001` y `SKN-001` no cuenten como productos distintos y dejé el mensaje de error en español. |

### Caso 2: Carrito en sesión con POST, CSRF y validación de stock (seguridad)

| Caso 2 | Carrito en sesión seguro |
|---|---|
| **Prompt** | En la guía que nos dio el profe, el carrito agrega, resta y elimina productos con links normales (GET). ¿Eso es seguro? ¿Cómo lo puedo hacer mejor en Django sin cambiar mucho la estructura? Además necesito que no deje agregar más cantidad que el stock que hay. |
| **Respuesta técnica** | Explicó que una petición GET no debe modificar datos, porque un enlace en otro sitio podría ejecutarla y el token CSRF no protege los GET. Recomendó usar formularios POST con `{% csrf_token %}`, limitar las vistas con `@require_POST`, marcar `request.session.modified = True` al cambiar el carrito y comparar la cantidad con `producto.stock` antes de agregar. |
| **Adaptación aplicada** | Mantuve las rutas de la guía (`agregar`, `restar`, `eliminar`, `limpiar`, `checkout`), pero las convertí a POST con CSRF, incluyendo vaciar el carrito y confirmar la compra. El checkout exige sesión iniciada con `@login_required` y vuelve a comprobar el stock antes de confirmar. Calculé el IVA del 19% con enteros (`subtotal * 19 // 100`), porque los precios están en pesos chilenos sin decimales. |

### Caso 3: `select_related` y búsqueda con `Q` (optimización de consultas)

| Caso 3 | Optimización del catálogo y búsqueda multicampo |
|---|---|
| **Prompt** | En mi catálogo cada tarjeta muestra la categoría del producto y me preocupa que haga una consulta por cada uno. Además la pauta pide buscar por título, código y descripción, y el buscador de la guía del profe solo busca en nombre, fabricante y categoría. ¿Cómo hago las dos cosas en Django? |
| **Respuesta técnica** | Indicó que `select_related('categoria')` trae la categoría en la misma consulta mediante un JOIN, evitando una consulta adicional por producto. Para la búsqueda propuso combinar objetos `Q` con el operador OR y el filtro `icontains`, de modo que el texto se busque en varios campos a la vez. También sugirió una lista de valores permitidos para el ordenamiento y usar `Paginator`. |
| **Adaptación aplicada** | Amplié la búsqueda de la guía a código, descripción y marca, además de nombre y categoría. Apliqué `select_related` en el catálogo, el detalle y el inventario, y `list_select_related` en el Django Admin. Mantuve la lista blanca de ordenamientos y la paginación de 6 productos, conservando la búsqueda, la categoría y el orden al cambiar de página. |