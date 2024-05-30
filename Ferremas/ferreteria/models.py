from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    # nro_cel = models.PositiveIntegerField()  # Elimina o comenta esta línea

class Bodeguero(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bodeguero')
    # nro_cel_bod = models.PositiveIntegerField()  # Elimina o comenta esta línea

class Contador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contador')
    # nro_cel_cont = models.PositiveIntegerField()  # Elimina o comenta esta línea

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Se añade el campo de imagen

    def __str__(self):
        return self.nombre

class CarroItem(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carro_items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cantidad} de {self.producto.nombre}'

    @property
    def subtotal(self):
        return self.cantidad * self.producto.precio