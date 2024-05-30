from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Cliente, Bodeguero, Contador, Producto


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('get_nombre', 'get_email', 'user_is_active')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user__is_active',)

    def get_nombre(self, obj):
        return obj.user.first_name

    def get_email(self, obj):
        return obj.user.email
    
    def user_is_active(self, obj):
        return obj.user.is_active
    user_is_active.boolean = True
    user_is_active.admin_order_field = 'user__is_active'

admin.site.register(Cliente, ClienteAdmin)

class BodegueroAdmin(admin.ModelAdmin):
    list_display = ('get_nombre', 'get_email', 'user_is_active')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user__is_active',)

    def get_nombre(self, obj):
        return obj.user.first_name

    def get_email(self, obj):
        return obj.user.email
    
    def user_is_active(self, obj):
        return obj.user.is_active
    user_is_active.boolean = True
    user_is_active.admin_order_field = 'user__is_active'

admin.site.register(Bodeguero, BodegueroAdmin)

class ContadorAdmin(admin.ModelAdmin):
    list_display = ('get_nombre', 'get_email', 'user_is_active')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user__is_active',)

    def get_nombre(self, obj):
        return obj.user.first_name

    def get_email(self, obj):
        return obj.user.email
    
    def user_is_active(self, obj):
        return obj.user.is_active
    user_is_active.boolean = True
    user_is_active.admin_order_field = 'user__is_active'

admin.site.register(Contador, ContadorAdmin)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'cantidad', 'imagen')
    list_editable = ('precio', 'cantidad')
    fields = ['nombre', 'descripcion', 'precio', 'cantidad', 'imagen']

    

