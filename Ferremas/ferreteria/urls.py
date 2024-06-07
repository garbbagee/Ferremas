from django.urls import path
from django.contrib import admin
from .views import index, compras, inise, formularioRegistro, vista_bod, agregar_al_carro, eliminar_del_carro, vista_paypal, execute_payment, payment_cancel
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
    path('agregar-al-carro/<int:producto_id>/', agregar_al_carro, name='agregar-al-carro'),
    path('eliminar-del-carro/<int:item_id>/', eliminar_del_carro, name='eliminar-del-carro'),
    path('pago/', vista_paypal, name='pago'),
    path('payment/execute/', execute_payment, name='payment_execute'),
    path('payment/cancel/', payment_cancel, name='payment_cancel'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)