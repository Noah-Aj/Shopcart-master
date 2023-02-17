from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50, null=True, verbose_name='Category Name')
    category_img = models.ImageField(upload_to='category_icons', verbose_name='Category Image', null=True)
    category_slug = models.CharField(max_length=50, null=True, verbose_name='Category Slug', unique=True)

    class Meta:
        ordering = ['category_name']
        indexes = [
            models.Index(fields=['category_name'])
        ]

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse('shop:category', args=[self.category_slug])


class Product(models.Model):
    prod_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Product Category', null=True)
    prod_name = models.CharField(max_length=50, null=True, verbose_name='Product Item')
    prod_slug = models.CharField(max_length=50, null=True, verbose_name='Product Slug')
    prod_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Product Price')
    prod_img = models.ImageField(upload_to='products/%d/%m/%Y', verbose_name='Product Image', null=True)
    prod_latest = models.BooleanField(default=False, verbose_name='Latest Product')
    prod_fresh = models.BooleanField(default=False, verbose_name='Fresh Product')
    prod_available = models.BooleanField(default=True, verbose_name='Available Product')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['prod_name']
        indexes = [
            models.Index(fields=['id', 'prod_slug']),
            models.Index(fields=['prod_name']),
            models.Index(fields=['-date_created'])
        ]

    def __str__(self):
        return self.prod_name

    def get_absolute_url(self):
        return reverse('shop:product', args=[self.prod_slug])


class Contact(models.Model):
    first_name = models.CharField(max_length=30, null=True, verbose_name='First Name', error_messages='Enter your first name', help_text='First Name')
    last_name = models.CharField(max_length=30, null=True, verbose_name='Last Name', error_messages='Enter your last name', help_text='Last name')
    email_user = models.EmailField(verbose_name='Email', error_messages='Enter a valid email address', help_text='Email Address')
    text_desc = models.TextField(null=True, verbose_name='Text', help_text='Enter your text', error_messages='Enter a text')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return self.first_name


class Subscribe(models.Model):
    email_user = models.EmailField(verbose_name='Email', error_messages='Enter a valid email address', help_text='Email Address')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['email_user']

    def __str__(self):
        return self.email_user


class SearchProduct(models.Model):
    prod_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Product Category', null=True)
    prod_name = models.CharField(max_length=50, null=True, verbose_name='Product Item')
    prod_slug = models.CharField(max_length=50, null=True, verbose_name='Product Slug')
    prod_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Product Price')
    prod_img = models.ImageField(upload_to='search/%d/%m/%Y', verbose_name='Product Image', null=True)

    class Meta:
        ordering = ['prod_name']
        indexes = [
            models.Index(fields=['id', 'prod_slug']),
            models.Index(fields=['prod_name']),
        ]

    def __str__(self):
        return self.prod_name

    def get_absolute_url(self):
        return reverse('shop:product', args=[self.prod_slug])