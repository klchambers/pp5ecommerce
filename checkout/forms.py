
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name',
            'email',
            'phone_number',
            'street_address1',
            'street_address2',
            'town_or_city',
            'postcode',
            'country',
            'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels, and set autofocus on first field
        """
        # Initialising default form
        super().__init__(*args, **kwargs)

        # defining form field placeholders
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # Sets focus to full_name field on page load
        self.fields['full_name'].widget.attrs['autofocus'] = True

        # iterate through fields adding asterisk to required fields
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders.get(field, field)} *'
            else:
                placeholder = placeholders.get(field, field)

            # adding placeholders to fields
            # Do not add placeholder to 'country' field
            if field != 'country':
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Adding CSS class
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # remove default labels
            self.fields[field].label = False

        # Add placeholder-like option for the country field
        # only for select fields to prevent w3c validation error
        if 'country' in self.fields:
            self.fields['country'].widget.choices = [('', 'Select your country')] + list(self.fields['country'].widget.choices)[1:] # noqa
