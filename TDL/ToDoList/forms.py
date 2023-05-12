from django import forms

class MyForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'username-field'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password-field'}))
