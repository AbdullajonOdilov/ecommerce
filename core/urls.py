from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static



app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # path('items/', AllItemAPIView.as_view(), name='items'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)