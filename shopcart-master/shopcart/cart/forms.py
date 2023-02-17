from django import forms

PRODUCT_QUANTITY = [(i, str(i)) for i in range(1, 21)]


class CartAddForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY, coerce=int
    )

    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
