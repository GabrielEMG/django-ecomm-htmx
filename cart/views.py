from django.shortcuts import render
from django.http import HttpResponse
from .models import Cart
from render_block import render_block_to_string

# Create your views here.
def index(request):
    cart = Cart.get_or_create_cart(request)
    cart_items = cart.cartitem_set.all()
    print(cart_items)
    return render(request, "cart_index.html", {"cart": cart, "cart_items": cart_items})


def add_to_cart(request, product_id):
    cart = Cart.get_or_create_cart(request)
    cart_item = cart.add_product(request, product_id)
    print(cart_item.quantity)
    html = render_block_to_string("cart_index.html", "cart_item", {"cart_item": cart_item})
    html += render_counter(request)
    html += render_total(request)
    return HttpResponse(html)

def remove_from_cart(request, product_id):
    cart = Cart.get_or_create_cart(request)
    cart_item = cart.remove_product(request, product_id)
    html = render_block_to_string("cart_index.html", "cart_item", {"cart_item": cart_item})
        
    html += render_counter(request)
    html += render_total(request)
    return HttpResponse(html)

def counter(request):
    return HttpResponse(render_counter(request))

def total(request):
    return HttpResponse(render_total(request))

def render_counter(request):
    return render_block_to_string("base.html", "cartcount", request=request)

def render_total(request):
    cart = Cart.get_or_create_cart(request)
    html = render_block_to_string("cart_index.html", "cart_total", {"total": cart.total()})
    return html
