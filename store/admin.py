from django.contrib import admin
from store.models import Category
from store.models import User
from store.models import Item

# Register your models here.

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Item)
