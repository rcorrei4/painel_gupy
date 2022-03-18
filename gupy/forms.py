from django import forms

class LoginForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'effect-16'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'effect-16'}))