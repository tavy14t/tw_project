from django import forms
# Create your models here.


class AuthForm(forms.Form):
    email = forms.CharField(
        label="Email", max_length=64, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
                               'placeholder': 'Your Email Adress'}))

    password = forms.CharField(
        label="Password", max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Password'}))


class UserForm(forms.Form):
    firstname = forms.CharField(
        label="First Name", max_length=64, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Your First Name'}))

    lastname = forms.CharField(label="Last Name", max_length=64, required=True,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Your Last Name'}))

    mail = forms.CharField(label="Mail Address", max_length=128, required=True,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control',
                                      'placeholder': 'Your Mail Address'}))

    password = forms.CharField(
        label="Password", max_length=128,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Password'}))
