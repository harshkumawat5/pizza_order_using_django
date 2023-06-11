from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls.static import static
# from django.conf import settings

from . import views
from django.conf import settings



urlpatterns = [
    path("home/",views.home,name="home" ),
    # path("delete_receipe/<id>/",views.delete_receipe,name="delete_receipe" ),
    # path("update_receipe/<id>/",views.update_receipe,name="update_receipe" ),
    path("register/",views.register_page,name="register" ),
    path("login/",views.login_page,name="login" ),
    path("addcart/<pizza_uid>",views.add_cart,name="addcart" ),
    path("cart/",views.cart,name="cart" ),
    path("remove_cart_item/<cart_item_uid>",views.remove_cart_item,name="remove_cart_item"),
    path("orders/",views.orders,name="orders"),
    path("success/",views.success,name="success"),
    path("logout/",views.logout_page,name="logout"),
    # path("logout/",views.logout_page,name="logout" ),
]

