from django.contrib import admin

# Register your models here.
from .models import Product, ProductType, ProductVariant, ProductMedia

admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(ProductVariant)
admin.site.register(ProductMedia)