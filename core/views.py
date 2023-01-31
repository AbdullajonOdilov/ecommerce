from requests import Response
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
from rest_framework import filters
from .models import *

# get
from .serializers import ItemSerializer


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'product.html', context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        # total = Order.get_total(self)
        context = {
            'form': form,
            # 'total': total
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                # region = form.cleaned_data.get('region')
                zip = form.cleaned_data.get('zip')
                image = form.cleaned_data.get('image')
                # TODO: add functionality for these fields
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                # payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    # region=region,
                    zip=zip,
                    image=image
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: add redirect to the selected payment option
                return redirect('core:checkout')
            messages.warning(self.request, "Failed")
            return redirect('core:checkout')
            return render(self.request, 'order_summary.html')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:order-summary")


# class PaymentView(View):
#     def get(self, *args, **kwargs):
#         total = Order.get_total()
#         context = {
#             'total': total
#         }
#         return render(self.request, 'payment.html', context)


class HomeView(View):
    paginate_by = 8

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title','category', 'description']
    def get(self, request):
        soz = request.GET.get('search')
        if soz is None:
            items = Item.objects.all()
        else:
            items = Item.objects.filter(
                title__contains=soz) | Item.objects.filter(
                category__contains=soz) | Item.objects.filter(
                description__contains=soz
            )
        context = {
            'object_list': items,
        }
        return render(request, 'home.html', context)


class ItemView(View):
    def get(self, request, filter):
        items = Item.objects.filter(category=filter)

        context = {

            'object_list': items
        }
        return render(request, 'home.html', context)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was added to your card")
            order.items.add(order_item)
            return redirect("core:order-summary")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your card")

        return redirect("core:product")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your card")
            return redirect("core:order-summary")
        else:
            # add a message saying the user does not contain the order
            messages.info(request, "This item was not in your card")
            return redirect("core:product", slug=slug)
    else:
        # add a message saying the user does not have an order
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quaantity was updated.")
            return redirect("core:order-summary")
        else:
            # add a message saying the user does not contain the order
            messages.info(request, "This item was not in your card")
            return redirect("core:product", slug=slug)
    else:
        # add a message saying the user does not have an order
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)
