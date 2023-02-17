from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email_user',
            'address', 'postal_code', 'city', 'phone_num',
        ]