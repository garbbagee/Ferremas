from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import ClienteForm
from django.contrib import messages
from .models import Cliente, Bodeguero, Contador, CarroItem, Producto
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from paypalrestsdk import Payment
import paypalrestsdk



def index(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    print(productos)  # Esto imprimirá la lista de productos en la consola donde se está ejecutando tu servidor
    return render(request, 'index.html', {'productos': productos})

def inise(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('index')  # Redirecciona a la página de inicio
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Nombre de usuario o contraseña inválidos.')
    else:
        form = AuthenticationForm()
    list(messages.get_messages(request))
    return render(request, 'inise.html', {'form': form})


def compras(request):
    return render(request, 'compras.html')


from django.contrib.auth.models import User
from .models import Cliente
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def formularioRegistro(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            try:
                form.save()  # Esto creará tanto el User como el Cliente
                
                return redirect('inise')  # Asegúrate de que 'index' es la URL a la que quieres redirigir.
            except Exception as e:
                messages.error(request, f'Error al crear la cuenta: {e}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = ClienteForm()
    return render(request, 'formularioRegistro.html', {'form': form})


def vista_bod(request):
    return render(request, 'vista_bod.html')




@login_required
def compras(request):
    items = CarroItem.objects.filter(usuario=request.user)  # Asume que 'CarroItem' tiene una relación con 'User'
    total = sum(item.producto.precio * item.cantidad for item in items)  # Calcula el total basándote en los ítems

    context = {
        'items': items,
        'total': total
    }
    return render(request, 'compras.html', context)

@login_required
def compras(request):
    items = CarroItem.objects.filter(usuario=request.user)
    total = sum(item.subtotal for item in items)
    return render(request, 'compras.html', {'items': items, 'total': total})



def agregar_al_carro(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carro_item, created = CarroItem.objects.get_or_create(
        usuario=request.user, 
        producto=producto,
        defaults={'cantidad': 1}
    )
    if not created:
        carro_item.cantidad += 1
        carro_item.save()
    return redirect('compras')


@login_required
def eliminar_del_carro(request, item_id):
    try:
        item = CarroItem.objects.get(id=item_id, usuario=request.user)
        item.delete()
        messages.success(request, "Producto eliminado del carro.")
    except CarroItem.DoesNotExist:
        messages.error(request, "El producto no se encontró en tu carro.")
    return redirect('compras')



def vista_paypal(request):
    return render(request, 'vista_paypal.html')

def create_payment(request):
    if request.method == "POST":
        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('payment_execute')),
                "cancel_url": request.build_absolute_uri(reverse('payment_cancel')),
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Item",
                        "sku": "item",
                        "price": "1.00",
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": "1.00",
                    "currency": "USD"
                },
                "description": "This is the payment transaction description."
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    return redirect(approval_url)
        else:
            print(payment.error)

    return render(request, 'pago.html')

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        print("Payment execute successfully")
        return render(request, 'payment_success.html')
    else:
        print(payment.error)
        return render(request, 'payment_error.html')

def payment_cancel(request):
    return render(request, 'payment_cancel.html')