from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    vendor = models.ForeignKey('vendor.Vendor', on_delete=models.CASCADE)
    type = models.ForeignKey('product.ProductType', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_first_variant(self):
        return self.productvariant_set.first()

    def get_sample_img(self):
        return self.productvariant_set.first().productmedia_set.first().image.url
    
    def get_lowest_price(self):
        return min([variant.price for variant in self.productvariant_set.all()])

    def get_variant_by_color(self, color):
        return self.productvariant_set.filter(color=color).first()

    def get_variants_by_colors(self):
        variants = []
        for variant in self.productvariant_set.all():
            if variant.color not in [v['color'] for v in variants]:
                variants.append({
                    'id': variant.id,
                    'color': variant.color,
                    'sizes': [v.size for v in self.productvariant_set.filter(color=variant.color)]
                })
        return variants

class ProductType(models.Model):
    name = models.CharField(max_length=100)
    sub_type = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return '{} - {}'.format(self.name, self.sub_type)
    
class ProductVariant(models.Model):
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    price = models.IntegerField()
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + ' - ' + self.color + ' - ' + self.size

    def get_first_media(self):
        return self.productmedia_set.first()
    
    def get_images(self):
        return self.productmedia_set.all()
    
    def cart_count(self, cart):
        return cart.cartitem_set.filter(product_id=self.id).first().quantity or 0

class ProductMedia(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images')
    product_variant = models.ForeignKey('product.ProductVariant', on_delete=models.CASCADE)

    def __str__(self):
        return self.product_variant.product.name + ' - ' + self.name + ' - ' + self.product_variant.color + ' - ' + self.product_variant.size