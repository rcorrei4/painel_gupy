from django.shortcuts import render

from .forms import LoginForm

def login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)

		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			print(email, password)
	else:
		return render(request, 'login.html', {
			"form": LoginForm()
			})