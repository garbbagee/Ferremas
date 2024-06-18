from django.urls import path
from django.contrib import admin
from .views import index, compras, inise, formularioRegistro, vista_bod, agregar_al_carro, eliminar_del_carro, vista_paypal, create_payment, execute_payment, payment_cancel
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('compras/', compras, name='compras'),
    path('inise/',inise, name='inise'),
    path('formularioRegistro/',formularioRegistro, name='formularioRegistro'),
    path('vista_bod/',vista_bod, name='vista_bod'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('agregar_al_carro/<int:producto_id>/', agregar_al_carro, name='agregar_al_carro'),
    path('eliminar_del_carro/<int:item_id>/', eliminar_del_carro, name='eliminar_del_carro'),
    path('pago/', vista_paypal, name='pago'),
    path('create_payment/', create_payment, name='create_payment'),
    path('execute_payment/', execute_payment, name='execute_payment'),
    path('payment_cancel/', payment_cancel, name='payment_cancel')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)