from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product/add_to_cart_pdp/<int:product_id>/<int:variant_id>", views.add_to_cart_pdp, name="add_to_cart_pdp"),
    path("product/remove_from_cart_pdp/<int:product_id>/<int:variant_id>", views.remove_from_cart_pdp, name="remove_from_cart_pdp"),
    path("product/<int:product_id>", views.product_page, name="product_page"),
    path("product_images/<str:filename>", views.product_image, name="product_image"),
    path("product/get_card_by_variant_id/<int:product_id>/<variant_id>", views.get_card_by_variant_id, name="get_card_by_variant_id"),
]
