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
from .paypal import paypalrestsdk


#from paypalrestsdk import Payment
#import paypalrestsdk



def index(request):
    productos = Producto.objects.using('productos_db').all()  # Obtener todos los productos desde productos_db
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





@login_required
def compras(request):
    user_id = request.user.id
    items = CarroItem.objects.using('productos_db').filter(usuario_id=user_id)
    total = sum(item.subtotal for item in items)
    return render(request, 'compras.html', {'items': items, 'total': total})


@login_required
def agregar_al_carro(request, producto_id):
    producto = get_object_or_404(Producto.objects.using('productos_db'), id=producto_id)
    user_id = request.user.id  # Obtén el ID del usuario de la base de datos predeterminada
    
    # Crear el CarroItem sin asignar el usuario directamente
    carro_item, created = CarroItem.objects.using('productos_db').get_or_create(
        usuario_id=user_id,
        producto=producto,
        defaults={'cantidad': 1}
    )
    if not created:
        carro_item.cantidad += 1
        carro_item.save(using='productos_db')
    return redirect('compras')

@login_required
def eliminar_del_carro(request, item_id):
    try:
        item = CarroItem.objects.using('productos_db').get(id=item_id, usuario_id=request.user.id)
        item.delete()
        messages.success(request, "Producto eliminado del carro.")
    except CarroItem.DoesNotExist:
        messages.error(request, "El producto no se encontró en tu carro.")
    return redirect('compras')


def vista_paypal(request):
    return render(request, 'vista_paypal.html')




@login_required
def create_payment(request):
    user_id = request.user.id
    items = CarroItem.objects.using('productos_db').filter(usuario_id=user_id)

    if not items:
        messages.error(request, "Tu carro está vacío.")
        return redirect('compras')

    total = sum(item.producto.precio * item.cantidad for item in items)
    transaction_items = [{
        "name": item.producto.nombre,
        "sku": str(item.producto.id),
        "price": str(item.producto.precio),
        "currency": "USD",
        "quantity": item.cantidad
    } for item in items]

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('payment_cancel')),
        },
        "transactions": [{
            "item_list": {
                "items": transaction_items
            },
            "amount": {
                "total": str(total),
                "currency": "USD"
            },
            "description": "Compra en Ferremas"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = link.href
                return redirect(approval_url)
    else:
        print(payment.error)
        messages.error(request, "Error al crear el pago con PayPal.")
        return redirect('compras')

@login_required
def create_payment(request):
    user_id = request.user.id
    items = CarroItem.objects.using('productos_db').filter(usuario_id=user_id)

    if not items:
        messages.error(request, "Tu carro está vacío.")
        return redirect('compras')

    total = sum(item.producto.precio * item.cantidad for item in items)
    transaction_items = [{
        "name": item.producto.nombre,
        "sku": str(item.producto.id),
        "price": str(item.producto.precio),
        "currency": "USD",
        "quantity": item.cantidad
    } for item in items]

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('payment_cancel')),
        },
        "transactions": [{
            "item_list": {
                "items": transaction_items
            },
            "amount": {
                "total": str(total),
                "currency": "USD"
            },
            "description": "Compra en Ferremas"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = link.href
                return redirect(approval_url)
    else:
        print(payment.error)
        messages.error(request, "Error al crear el pago con PayPal.")
        return redirect('compras')

@login_required
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        print("Payment executed successfully")
        # Aquí puedes vaciar el carro del usuario o registrar el pago en tu base de datos
        CarroItem.objects.using('productos_db').filter(usuario_id=request.user.id).delete()
        return render(request, 'payment_success.html')
    else:
        print(payment.error)
        return render(request, 'payment_error.html')

def payment_cancel(request):
    return render(request, 'payment_cancel.html')









from django.shortcuts import render
from .models import Producto

def listar_productos(request):
    productos = Producto.objects.using('productos_db').all()
    return render(request, 'productos/listar_productos.html', {'productos': productos})

from django.shortcuts import render, redirect
from .forms import ProductoForm


def vista_bod(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear una instancia del modelo Producto sin guardarla aún en la base de datos
            nuevo_producto = form.save(commit=False)
            # Guardar la instancia del producto en la base de datos 'productos_db'
            nuevo_producto.save(using='productos_db')
            return redirect('vista_bod')  # Redirige a la misma vista o a otra que prefieras
    else:
        form = ProductoForm()

    # Aquí puedes agregar más lógica si necesitas mostrar más información en la plantilla
    context = {
        'form': form,
        # Otros contextos que quieras pasar a la plantilla
    }
    return render(request, 'vista_bod.html', context)

