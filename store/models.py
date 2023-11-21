from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("name",)


class Item(models.Model):
    name = models.CharField(max_length=200)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='media/')
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='CartItem')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.selling_price * self.quantity

    class Meta:
        unique_together = ('cart', 'product')  # Ensure uniqueness of wishlist items


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wishlist', 'product')  # Ensure uniqueness of wishlist items