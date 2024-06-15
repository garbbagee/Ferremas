class ProductosRouter:
    """
    Un router para controlar todas las operaciones de base de datos para el modelo de productos.
    """
    route_app_labels = {'productos'}

    def db_for_read(self, model, **hints):
        """
        Intenta leer el modelo de productos desde 'productos_db'.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'productos_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Intenta escribir el modelo de productos en 'productos_db'.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'productos_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permitir relaciones si un modelo en 'productos_db' está involucrado.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Asegurarse de que los modelos de 'productos' se migren solo a 'productos_db'.
        """
        if app_label in self.route_app_labels:
            return db == 'productos_db'
        return None
