from django.shortcuts import render, redirect
from store.models import Item


# Create your views here.


def index(request):
    items = Item.objects.all()
    return render(request, "store/index.html", {"items":items})
