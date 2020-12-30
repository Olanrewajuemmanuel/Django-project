from django import forms


class UserForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=254)
    phone_number = forms.CharField(max_length=14)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput())

class LoginForm(forms.Form):
    email = forms.CharField(max_length=254)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput())
