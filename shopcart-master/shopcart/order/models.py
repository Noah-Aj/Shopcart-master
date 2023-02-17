from django.db import models
from shop.models import Product
from .utils import generate_code

# Create your models here.


class Order(models.Model):
    order_id = models.CharField(max_length=9, blank=True)
    first_name = models.CharField(max_length=30, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=30, null=True, verbose_name='Last Name')
    email_user = models.EmailField(verbose_name='Email Address')
    address = models.CharField(max_length=200, null=True, verbose_name='Home Address')
    postal_code = models.CharField(max_length=30, null=True, verbose_name='Postal Code')
    city = models.CharField(max_length=30, null=True, verbose_name='City')
    phone_num = models.CharField(max_length=30, null=True, verbose_name='Phone Number')
    paid = models.BooleanField(default=False, verbose_name='Paid')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def get_total_sum(self):
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self):
        return f'{self.first_name[:3]}{self.last_name[:3]}{self.id}'

    def save(self, *args, **kwargs):
        if self.order_id == "":
            order_id = generate_code()
            self.order_id = order_id
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        total = self.price * self.quantity
        return total

    def __str__(self):
        return str(self.id)
