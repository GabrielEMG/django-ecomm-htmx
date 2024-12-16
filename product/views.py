from django.shortcuts import render
from .models import Product, ProductVariant
from cart.models import Cart
from django.template import loader

from cart.views import render_counter

from django.http import HttpResponse
from render_block import render_block_to_string


def index(request):
    products = Product.objects.all()
    cart = Cart.get_or_create_cart(request)
    context = {
        "products": products,
        "cart": cart,
    }
    
    return render(request, "product/plp.html", context)


def product_page(request, product_id):
    variant_id=request.GET.get('v')
    if variant_id:
        variant = ProductVariant.objects.get(id=variant_id)
    else:
        variant = ProductVariant.objects.filter(product_id=product_id).first().id
    product = Product.objects.get(id=product_id)
    cart = Cart.get_or_create_cart(request)
    cart_item = cart.cartitem_set.filter(product_id=variant_id).first()
    context = {
        "product": product,
        "cart": cart,
        "cart_item": cart_item,
        "variant": variant
    }
    return render(request, "product/pdp.html", context)


def add_to_cart_pdp(request, product_id, variant_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.get_or_create_cart(request)
    cart.add_product(request, variant_id)
    cart_item = cart.cartitem_set.filter(product_id=variant_id).first()
    variant = ProductVariant.objects.get(id=variant_id)
    html = render_block_to_string("product/pdp.html", "variant_add_to_cart", {
        "cart": cart,
        "product": product,
        "cart_item": cart_item,
        "variant": variant
    })
    html += render_counter(request)
    return HttpResponse(html)

def remove_from_cart_pdp(request, product_id, variant_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.get_or_create_cart(request)
    cart.remove_product(request, variant_id)
    cart_item = cart.cartitem_set.filter(product_id=variant_id).first()
    variant = ProductVariant.objects.get(id=variant_id)
    html = render_block_to_string("product/pdp.html", "variant_add_to_cart", {
        "cart": cart,
        "product": product,
        "cart_item": cart_item,
        "variant": variant
    })
    html += render_counter(request)
    return HttpResponse(html)

def product_image(request, filename):
    with open(f"product_images/{filename}", "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")

def get_card_by_variant_id(request, product_id, variant_id):
    product = Product.objects.get(id=product_id)
    product_variant = ProductVariant.objects.get(id=variant_id)
    print(product_variant)
    html = render_block_to_string("product/plp.html", "product_card", {
        "product": product,
        "variant": product_variant,
    })
    return HttpResponse(html)