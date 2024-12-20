from django import forms
from .models import Wine, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Wine
        fields = '__all__'
        exclude = ['slug']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        """Set the category field as a
        ModelMultipleChoiceField for the ManyToManyField"""
        self.fields['category'] = forms.ModelMultipleChoiceField(
            queryset=Category.objects.all(),
            # Allows selecting multiple options
            widget=forms.CheckboxSelectMultiple,
            required=False
        )
