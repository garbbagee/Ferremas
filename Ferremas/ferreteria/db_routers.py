# ferreteria/db_routers.py

class ProductosRouter:
    """
    Un enrutador de bases de datos para controlar las operaciones de base de datos
    para los modelos relacionados con productos y usuarios.
    """

    def db_for_read(self, model, **hints):
        """
        Intentar leer el modelo desde 'productos_db' para productos y 'default' para usuarios.
        """
        if model._meta.app_label == 'ferreteria':
            return 'productos_db'
        elif model._meta.app_label == 'auth':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """
        Intentar escribir el modelo en 'productos_db' para productos y 'default' para usuarios.
        """
        if model._meta.app_label == 'ferreteria':
            return 'productos_db'
        elif model._meta.app_label == 'auth':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permitir relaciones si ambos modelos están en 'ferreteria' o 'auth'.
        """
        if (obj1._meta.app_label in ['ferreteria', 'auth'] and
                obj2._meta.app_label in ['ferreteria', 'auth']):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Asegurarse de que la aplicación 'ferreteria' y 'auth' solo aparecen en la base de datos correspondientes.
        """
        if app_label == 'ferreteria':
            return db == 'productos_db'
        elif app_label == 'auth':
            return db == 'default'
        return None
