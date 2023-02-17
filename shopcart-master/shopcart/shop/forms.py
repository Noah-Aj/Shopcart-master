from .models import Contact, Subscribe
from django import forms


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name', 'email_user', 'text_desc'
        ]


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email_user']
