from django.contrib import admin
from .models import Category, Product, Contact, Subscribe, SearchProduct

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_img', 'category_name', 'category_slug']
    list_editable = ['category_name']
    prepopulated_fields = {
        'category_slug': ("category_name",)
    }


@admin.register(Product)
class ProdustAdmin(admin.ModelAdmin):
    list_display = ['prod_name', 'prod_category', 'prod_price', 'prod_latest', 'prod_available', 'prod_fresh']
    list_filter = ['prod_name', 'prod_price', 'prod_available']
    list_editable = ['prod_price', 'prod_available', 'prod_latest', 'prod_fresh']
    prepopulated_fields = {
        'prod_slug': ('prod_name',)
    }


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email_user']
    list_filter = ['date_created']


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['email_user']
    list_filter = ['date_created']


@admin.register(SearchProduct)
class SearchAdmin(admin.ModelAdmin):
    list_display = ['prod_name', 'prod_category', 'prod_price']
    list_filter = ['prod_name', 'prod_price']
    list_editable = ['prod_price']
    prepopulated_fields = {
        'prod_slug': ('prod_name',)
    }
