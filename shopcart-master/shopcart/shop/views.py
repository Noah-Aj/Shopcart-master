from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from .models import Category, Product, Subscribe, SearchProduct
from cart.forms import CartAddForm
from .forms import ContactForm, SubscribeForm
from django.contrib import messages
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

# Create your views here.


def product_list(request):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all().filter(prod_available=True)
    related_search = SearchProduct.objects.all()[:12]
    fresh_product = Product.objects.all().filter(prod_fresh=True)[:6]
    cart_product_form = CartAddForm()
    subscribe_form = SubscribeForm()

    return render(request, 'index.html', {
        'category': category,
        'related': related_search,
        'fresh': fresh_product,
        'categories': categories,
        'products': products,
        'cart_form': cart_product_form,
        'subscribe_form': subscribe_form
    })


def product_category_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all().filter(prod_available=True)
    cart_product_form = CartAddForm()
    subscribe_form = SubscribeForm()
    related_search = SearchProduct.objects.all()[:12]

    if category_slug:
        category = get_object_or_404(Category, category_slug=category_slug)
        products = products.filter(prod_category=category)
    return render(request, 'category.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'cart_form': cart_product_form,
        'subscribe_form': subscribe_form,
        'related': related_search
    })


def product_detail(request, product_slug):
    context = {}
    product = get_object_or_404(Product, prod_slug=product_slug, prod_available=True)
    cart_product_form = CartAddForm()
    context['product'] = product
    context['related'] = SearchProduct.objects.all()[:12]
    context['cart_form'] = cart_product_form
    context['subscribe_form'] = SubscribeForm
    return render(request, 'product_detail.html', context)


# def fresh_products(request):
#     fresh_product = Product.objects.all().filter(prod_fresh=True)
#     cart_product_form = CartAddForm()
#     subscribe_form = SubscribeForm()
#     related_search = SearchProduct.objects.all()[:12]
#
#     context = {
#         'fresh': fresh_product,
#         'related': related_search,
#         'cart_form': cart_product_form,
#         'subscribe_form': subscribe_form
#     }
#     return render(request, "fresh.html", context)


def contact(request):
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            first_name = contact_form.cleaned_data.get('first_name')
            last_name = contact_form.cleaned_data.get('last_name')
            email_user = contact_form.cleaned_data.get('email_user')

            full_name = first_name + " " + last_name
            success_message = f'{full_name}, your message has been received. Thank you'
            messages.success(request, success_message)

            # send email
            template = render_to_string('contact_email.html', {'email': email_user})
            email_send = EmailMessage(
                'Your message was successful!',
                template,
                settings.EMAIL_HOST_USER,
                [email_user]
            )
            email_send.fail_silently = False
            email_send.send()

            return redirect('shop:contact')
    else:
        contact_form = ContactForm()
        subscribe_form = SubscribeForm()

        context = {
            'form': contact_form,
            'subscribe_form': subscribe_form
        }
        return render(request, 'contact.html', context)


def subscribe(request):
    if request.method == "POST":
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            email_user = str(subscribe_form.cleaned_data.get('email_user'))
            if Subscribe.objects.filter(email_user=email_user).exists():
                err_message = f'You are already a subscriber {email_user.lower()}'
                messages.error(request, err_message)
                return redirect('shop:product_list')
            else:
                subscribe_form.save()
                success_message = f'You will receive information on our new stocked items via {email_user.lower()}.\n Thank you for subscribing.'
                messages.success(request, success_message)
                return redirect('shop:product_list')


def search_products(request):
    products = Product.objects.filter(prod_available=True).filter(prod_fresh=True).values_list('prod_name', flat=True)
    products_list = list(products)
    return JsonResponse(products_list, safe=False)


def searched_products(request):
    cart_product_form = CartAddForm()
    related_search = SearchProduct.objects.all()[:12]
    if request.method == "POST":
        search_product = request.POST.get("search-me")
        if search_product == "":
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            product = Product.objects.filter(prod_name__icontains=search_product).first()
            if product:
                related_product, created = SearchProduct.objects.update_or_create(
                    prod_category=product.prod_category, prod_name=product.prod_name, prod_slug=product.prod_slug,
                    prod_price=product.prod_price, prod_img=product.prod_img
                )
                related_product.save()
                return render(request, "search_detail.html", {'product': product, 'cart_form': cart_product_form, 'related': related_search})
            else:
                messages.info(request, "No product")
                return HttpResponseRedirect(reverse("shop:product_list"))
    return redirect(request.META.get("HTTP_REFERER"))
