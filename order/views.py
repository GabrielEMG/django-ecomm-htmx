from django.shortcuts import render
from .models import Order
from cart.models import Cart

# Create your views here.
def index(request):
    cart = Cart.get_or_create_cart(request)
    return render(request, "index.html", {"cart": cart})

def create_order(request):
    if request.method == "POST":
        order = Order.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            address=request.POST.get("address"),
            cart_id=request.session.get("cart_id")
        )
        return render(request, "order_confirmation.html", {
            "order": order,
        })