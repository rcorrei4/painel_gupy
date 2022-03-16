from bs4 import BeautifulSoup
import requests

from django.shortcuts import render

from .forms import LoginForm

def login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)

		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			session = requests.Session()

			payload = {
			    'email': email, 
			    'password': password,
			    'subdomain': 'login'
			    }

			s = session.post("https://private-api.gupy.io/authentication/candidate/account/signin", data=payload)
			response = s.json()
			print(response.get('token'))
	else:
		return render(request, 'login.html', {
			"form": LoginForm()
			})