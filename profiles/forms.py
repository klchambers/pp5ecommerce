from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = {'user', }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        # initialising default form
        super().__init__(*args, **kwargs)
        # defining form field placeholders
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_country': 'Country',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County',
        }

        # Sets focus to full_name field on page load
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        # iterate through fields adding asterisk to required fields
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                # adding placeholders to fields
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Adding CSS class
            self.fields[field].widget.attrs['class'] = 'profile-form-input'
            # remove default labels
            self.fields[field].label = False
