from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddForm
from shop.models import Product, SearchProduct
from shop.forms import SubscribeForm

# Create your views here.


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        cart.add(
            product=product,
            quantity=form_data['quantity'],
            override_quantity=form_data['override']
        )
    return redirect('shop:category')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    subscribe_form = SubscribeForm()
    related_search = SearchProduct.objects.all()[:12]
    for item in cart:
        item['update_quantity'] = CartAddForm(
            initial={
                'quantity': item['quantity'],
                'override': True
            }
        )
    context = {
        'cart': cart,
        'subscribe_form': subscribe_form,
        'related': related_search
    }
    return render(request, 'detail.html', context)

