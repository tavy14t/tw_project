from django import forms
# Create your models here.


class User(forms.Form):
    firstname = forms.CharField(
        label="First Name", max_length=64, required=True)
    lastname = forms.CharField(label="Last Name", max_length=64, required=True)
    mail = forms.CharField(label="Mail Address", max_length=128, required=True)
    password = forms.CharField(
        label="Password", max_length=128,
        required=True, widget=forms.PasswordInput())
