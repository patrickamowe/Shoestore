from django.contrib import admin
from store.models import Category
from store.models import User
from store.models import Item
from store.models import Cart, CartItem, Wishlist, WishlistItem, ProductView

# Register your models here.
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)
admin.site.register(ProductView)


@admin.register(Category)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_display_links = ('id', 'name')
    list_per_page = 20


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'username', 'is_superuser', 'is_active')
    list_filter = ('is_superuser', 'is_active')
    list_display_links = ('id', 'first_name', 'last_name', 'email', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "password", "is_superuser", "state", "is_staff")
        }
         ),
    )
    list_per_page = 10
