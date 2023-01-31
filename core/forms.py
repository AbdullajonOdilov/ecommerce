from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

REGION_CHOICES = (
    ('A', 'Andijon'),
    ('B', 'Bukhara'),
    ('F', 'Fergana'),
    ('N', 'Namangan'),
    ('Na', 'Navoi'),
    ('J', 'Jizzax'),
    ('Sa', 'Samarqand'),
    ('S', 'Sirdarya'),
    ('Su', 'Surkhandarya'),
    ('Q', 'Qashqadaryo'),
    ('Qa', 'Qoraqalpagistan'),
    ('T', 'Tashkent city'),
    ('Ta', 'Tashkent'),

    ('X', 'Xarazm'),
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Moturidiy 32/1'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite'
    }))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'
    }))

    # region = forms.ChoiceField(blank_label='(select region)').formfield(widget=forms.RadioSelect(attrs={
    #     'class': 'custom-select d-block w-100'
    # }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    image = forms.FileField(required=True)
    # payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
