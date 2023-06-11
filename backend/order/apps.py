from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "order"


    def ready(self):
        from django.contrib.auth.models import User
        def cart_count(self):
            from .models import CartItems
            return CartItems.objects.filter(cart__is_paid=False,cart__user=self).count()
        User.add_to_class("cart_count",cart_count)