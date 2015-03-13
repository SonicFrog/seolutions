from django import forms


class UserLoginForm(forms.Form):
    login = forms.CharField()
    password = forms.PasswordInput()
