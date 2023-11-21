from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('signup', views.signup, name="register"),
    path('logout', views.logout_view, name="logout"),
    path('detail/<int:id>', views.detail, name="detail"),
    path('view_cart', views.view_cart, name="view_cart"),
    path('view_wishlist', views.view_wishlist, name="view_wishlist"),

    #API rounte
    path('add_to_cart/<int:id>', views.add_to_cart, name="add_to_cart"),
    path('add_to_wishlist/<int:id>', views.add_to_wishlist, name="add_to_wishlist"),
    path('delete_item/<int:id>', views.remove_item_from_cart, name="delete_item"),
    path('remove_from_wishlist/<int:id>', views.remove_from_wishlist, name="remove_from_wishlist"),

]