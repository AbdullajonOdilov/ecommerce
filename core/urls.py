from django.urls import path
from .views import *

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('items/<str:filter>', ItemView.as_view(), name='filter'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    # path('payment/', PaymentView.as_view(), name='payment')
]
