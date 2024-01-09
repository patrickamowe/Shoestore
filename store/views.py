from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from store.models import Item, User, Cart, CartItem, WishlistItem, Wishlist, Category, ProductView
import logging


# Create your views here.

def index_view(request):
    user = request.user
    items = Item.objects.all()[:8]
    most_recent_posts = Item.objects.order_by('-timestamp')[:5]

    user_views = []
    cart_items = []
    sub_total = 0

    if user.is_authenticated:

        user_views = ProductView.objects.filter(user=request.user)[:5]

        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            sub_total = sum(item.product.selling_price * item.quantity for item in cart_items)

        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)

    return render(request, "store/index.html", {"items":items, "most_recent_posts":most_recent_posts, "user_views": user_views, "cart_items": cart_items, "sub_total": sub_total})


def about_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        sub_total = sum(item.product.selling_price * item.quantity for item in cart_items)

    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
        cart_items = []
        sub_total = 0

    return render(request, "store/about-us.html", {"sub_total": sub_total, "cart_items": cart_items})


@login_required
def order_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        sub_total = sum(item.product.selling_price * item.quantity for item in cart_items)

    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
        cart_items = []
        sub_total = 0

    return render(request, "store/order.html", {"sub_total": sub_total, "cart_items": cart_items})


def shop_view(request):
    user = request.user
    items = Item.objects.all()
    paginator = Paginator(items, 12)  # Show 12 items per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cart_items = []
    sub_total = 0

    if user.is_authenticated:

        try:
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)
            sub_total = sum(item.product.selling_price * item.quantity for item in cart_items)

        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)

    return render(request, "store/shop.html", {"page_obj":page_obj, "cart_items": cart_items, "sub_total": sub_total})


def detail_view(request, id):
    user = request.user
    item = Item.objects.get(id=id)
    category = item.category
    same_categories = Item.objects.filter(category=category)[:4]
    cart_items = []
    sub_total = 0

    if user.is_authenticated:

        ProductView.objects.get_or_create(user=user, product=item)
        try:
            cart = Cart.objects.get(user=user)
            cart_items = CartItem.objects.filter(cart=cart)
            sub_total = sum(item.product.selling_price * item.quantity for item in cart_items)

        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)

    return render(request, "store/detail.html", {'item': item, 'same_categories': same_categories, "cart_items": cart_items, "sub_total": sub_total})


def account_view(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        sub_total = sum(item.product.selling_price * item.quantity for item in cart_items)

    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
        cart_items = []
        sub_total = 0

    return render(request, "store/account.html", {"sub_total": sub_total, "cart_items": cart_items})


@login_required
def checkout_view(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        sub_total = sum(item.product.selling_price * item.quantity for item in cart_items)

    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
        cart_items = []
        sub_total = 0

    return render(request, "store/checkout.html", {"cart_items": cart_items, "sub_total": sub_total})


def error_404_view(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        sub_total = sum(item.product.selling_price * item.quantity for item in cart_items)

    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
        cart_items = []
        sub_total = 0

    return render(request, "store/404.html", {"sub_total": sub_total, "cart_items": cart_items})


def pop_login(request):

    return render(request, "store/ajax/login.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["signin-username"]
        password = request.POST["signin-password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "store/login.html", {
                "message": "Invalid username or password."
            })
    else:
        return render(request, "store/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def signup(request):
    if request.method == "POST":
        username = request.POST["register-username"]
        email = request.POST["register-email"]

        # Ensure password matches confirmation
        password = request.POST["register-password"]
        confirmation = request.POST["register-confirmation"]
        if password != confirmation:
            return render(request, "store/login.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "store/login.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "store/login.html")


def add_to_cart(request, id):
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = Item.objects.get(id=id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        cart.total += product.selling_price
        cart.save()

        # Return a success message
        response_data = {'status': 'success', 'message': 'Item added to cart successfully.'}
        return JsonResponse(response_data)

    except Exception as e:
        # Return a failure message
        response_data = {'status': 'fail', 'message': str(e)}
        return JsonResponse(response_data, status=500)


@login_required
def view_cart(request):
    user = request.user
    if user.is_anonymous:
        return HttpResponseRedirect(reverse("login"))
    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        sub_total = sum(item.product.selling_price * item.quantity for item in cart_items)
        row_totals = [item.product.selling_price * item.quantity for item in cart_items]
        zip_list = zip(cart_items,row_totals)
        total = sub_total + 30
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
        cart_items = []
        sub_total = 0

    return render(request, 'store/cart.html', {'cart_items': cart_items, 'sub_total': sub_total, 'total': total, 'zip_list': zip_list})


logger = logging.getLogger(__name__)


def remove_from_cart(request, id):
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    product = get_object_or_404(Item, id=id)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        price = cart_item.quantity * product.selling_price
        cart.total -= price
        cart.save()
        cart_item.delete()
        response_data = {'status': 'success', 'message': 'Item deleted from cart successfully.'}
        return JsonResponse(response_data, status=200)

    except CartItem.DoesNotExist:
        response_data = {'status': 'fail', 'message': 'Item not found in the cart'}
        return JsonResponse(response_data, status=404)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        response_data = {'status': 'fail', 'message': 'An error occurred.'}
        return JsonResponse(response_data, status=500)


def add_to_wishlist(request, id):
    try:
        wishlist, created_wishlist = Wishlist.objects.get_or_create(user=request.user)
        product = Item.objects.get(id=id)
        wishlist_item, created_wishlist_item = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)

        if created_wishlist or created_wishlist_item:
            # Return a success message with a status code 201 (Created)
            response_data = {'status': 'success', 'message': 'Item added to wishlist successfully.'}
            return JsonResponse(response_data, status=201)
        else:
            # Return a success message (item already in the wishlist) with a status code 200 (OK)
            response_data = {'status': 'success', 'message': 'Item already exists in the wishlist.'}
            return JsonResponse(response_data, status=200)

    except Item.DoesNotExist:
        # Return a failure message with a status code 404 (Not Found)
        response_data = {'status': 'fail', 'message': 'Product not found.'}
        return JsonResponse(response_data, status=404)

    except IntegrityError:
        # Handle IntegrityError specifically (e.g., item already in the wishlist) with a status code 400 (Bad Request)
        response_data = {'status': 'fail', 'message': 'Item already exists in the wishlist.'}
        return JsonResponse(response_data, status=400)

    except Exception as e:
        # Return a generic failure message with a status code 500 (Internal Server Error)
        response_data = {'status': 'fail', 'message': str(e)}
        return JsonResponse(response_data, status=500)


def view_wishlist(request):
    user = request.user
    if user.is_anonymous:
        return HttpResponseRedirect(reverse("login"))
    try:
        wishlist = Wishlist.objects.get(user=user)
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(user=user)
        wishlist_items = []

    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        sub_total = sum(item.product.selling_price * item.quantity for item in cart_items)

    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
        cart_items = []
        sub_total = 0

    return render(request, 'store/wishlist.html', {'wishlist': wishlist, 'wishlist_items':wishlist_items, "cart_items": cart_items, "sub_total": sub_total})


def remove_from_wishlist(request, id):
    user = request.user
    wishlist = get_object_or_404(Wishlist, user=user)
    product = get_object_or_404(Item, id=id)

    try:
        wishlist_item = WishlistItem.objects.get(wishlist=wishlist, product=product)
        wishlist_item.delete()
        response_data = {'status': 'success', 'message': 'Item deleted from wishlist successfully.'}
        return JsonResponse(response_data, status=200)

    except WishlistItem.DoesNotExist:
        response_data = {'status': 'fail', 'message': 'Item not found in the cart'}
        return JsonResponse(response_data, status=404)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        response_data = {'status': 'fail', 'message': 'An error occurred.'}
        return JsonResponse(response_data, status=500)


def category_view(request, category):
    user = request.user
    id = Category.objects.get(name=category)
    items = Item.objects.filter(category=id)
    paginator = Paginator(items, 12)  # Show 12 items per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cart_items = []
    sub_total = 0

    if user.is_authenticated:

        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            sub_total = sum(item.product.selling_price * item.quantity for item in cart_items)

        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)

    return render(request, 'store/category.html', {'page_obj': page_obj, "cart_items": cart_items, "sub_total": sub_total})