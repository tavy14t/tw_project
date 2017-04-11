from __future__ import unicode_literals

from django import forms


class SearchForm(forms.Form):
    string = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'search_text'
            }
        )
    )
