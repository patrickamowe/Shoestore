from . import views
from django.urls import path

urlpatterns = [
    path('', views.index_view, name="index"),
    path('login', views.login_view, name="login"),
    path('pop_login', views.pop_login, name="pop_login"),
    path('signup', views.signup, name="register"),
    path('logout', views.logout_view, name="logout"),
    path('about_view', views.about_view, name='about_view'),
    path('shop', views.shop_view, name="shop_view"),
    path('detail/<int:id>', views.detail_view, name="detail_view"),
    path('account_view', views.account_view, name="account_view"),
    path('wishlist_view', views.view_wishlist, name="wishlist_view"),
    path('checkout_view', views.checkout_view, name="checkout_view"),
    path('error_404', views.error_404_view, name="error_404"),
    path('order', views.order_view, name="order"),
    path('view_cart', views.view_cart, name="view_cart"),
    path('view_wishlist', views.view_wishlist, name="view_wishlist"),
    path('category/<str:category>/', views.category_view, name="category_view"),

    # API route
    path('add_to_cart/<int:id>', views.add_to_cart, name="add_to_cart"),
    path('add_to_wishlist/<int:id>', views.add_to_wishlist, name="add_to_wishlist"),
    path('remove_from_wishlist/<int:id>', views.remove_from_wishlist, name="remove_from_wishlist"),
    path('remove_from_cart/<int:id>', views.remove_from_cart, name="remove_from_cart"),

]