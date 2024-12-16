from django.db import models

# Create your models here.
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    
    def get_or_create_cart(request):
        cart_id = request.session.get("cart_id")
        if not cart_id:
            cart = Cart.objects.create()
            request.session["cart_id"] = cart.id
        else:
            cart = Cart.objects.get(id=cart_id)
        request.session["cart_count"] = cart.quantity()
        return cart

    def items(self):
        return self.cartitem_set.all()
    
    def total(self):
        total = 0
        for item in self.items():
            total += item.total()
        total = "{:,}".format(int(total)).replace(",", ".")
        return total
    
    def randomtwo(self):
        return "random3"

    def quantity(self):
        quantity = 0
        for item in self.items():
            quantity += item.quantity
        return quantity
    

    def add_product(self, request, variant_id):
        print("variant_id:" , variant_id)
        cart_item = self.cartitem_set.filter(product_id=variant_id).first()
        if cart_item:
            cart_item.add_quantity(1)
        else:
            cart_item = CartItem.objects.create(cart=self, product_id=variant_id, quantity=1)
        request.session["cart_count"] = self.quantity()
        return cart_item

    def remove_product(self, request, variant_id):
        cart_item = self.cartitem_set.filter(product_id=variant_id).first()
        if cart_item:
            if cart_item.quantity == 1:
                cart_item.quantity = 0
                cart_item.delete()
            else:
                cart_item.add_quantity(-1)
        request.session["cart_count"] = self.quantity()
        return cart_item

class CartItem(models.Model):
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('product.ProductVariant', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cart} - {self.product} - {self.quantity}"
    
    def total(self):
        return self.product.price * self.quantity
    
    def add_quantity(self, quantity):
        self.quantity += quantity
        self.save()