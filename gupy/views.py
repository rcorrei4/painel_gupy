import requests
import json
from bs4 import BeautifulSoup

from django.shortcuts import render, redirect

from .forms import LoginForm

def login(request):
	if request.method == "POST":
		form = LoginForm(request.POST)

		if form.is_valid():
			email = form.cleaned_data['email']
			senha = form.cleaned_data['password']

			payload = {
				'email': email, 
				'password': senha,
				'subdomain': 'login'
				}

			r = requests.post("https://private-api.gupy.io/authentication/candidate/account/signin", data=payload)
			response = r.json()

			request.session['token'] = response.get('token')
			
			return redirect('index')
	else:
		return render(request, 'login.html', {
			"form": LoginForm()
			})

def index(request):
	if request.session['token']:
		candidaturas = pegar_informacoes(request.session.get('token'))

		return render(request, 'index.html', {
			'candidaturas': candidaturas
			})
	else:
		return redirect('login')

def pegar_informacoes(token):

	# Pegar as informações sobre o usuário
	headers = {
		'candidate_key': token,
		'origin': 'https://login.gupy.io',
		'refer': 'https://login.gupy.io/',
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
		}

	info_user = requests.get(
		'https://private-api.gupy.io/authentication/candidate/account/current', 
		headers=headers
		)
	info_user = info_user.json()

	candidaturas = dict()

	# Pegar o domínio gupy de cada empresa onde o usuário se candidatou
	for empresa in info_user['careerPages']:
		dominio_empresa = empresa['subdomain']

		candidaturas[dominio_empresa] = {
			'nome': empresa['name'],
			'candidaturas': pegar_candidaturas(token, dominio_empresa)
		}

	# print(json.dumps(candidaturas, sort_keys=False, indent=4))

def pegar_candidaturas(token, dominio_empresa):
	headers = {
		'candidate_key': token,
		'origin': f'https://{dominio_empresa}.gupy.io',
		'refer': f'https://{dominio_empresa}.gupy.io/',
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
		}

	# Pegar todas as candidaturas do usuário na empresa
	candidaturas_empresa = requests.get(
		'https://private-api.gupy.io/selection-process/candidate/application', 
		headers=headers
		)
	candidaturas_empresa = candidaturas_empresa.json()

	# Dicionário para armazenar as candidaturas feitas na empresa
	candidaturas = dict()

	for candidatura in candidaturas_empresa['data']:
		candidatura_id = candidatura['applicationId']

		info_candidatura = pegar_info_candidaturas(token, dominio_empresa, candidatura['applicationId'])
		candidaturas[candidatura_id] = {
			'id': candidatura['applicationId'],
			'nome': candidatura['name'],
			'testes': candidatura['jobStepCount'],
			'teste_em_andamento': {
				'id': info_candidatura['id'],
				'teste': candidatura['jobStepCurrent'],
				'nome': info_candidatura['nome'],
				'descricao': info_candidatura['descricao']
			},
		}

	return candidaturas

def pegar_info_candidaturas(token, dominio_empresa, id_candidatura):
	headers = {
		'candidate_key': token,
		'origin': f'https://{dominio_empresa}.gupy.io',
		'refer': f'https://{dominio_empresa}.gupy.io/',
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
		}

	info_candidatura = requests.get(
		f'https://private-api.gupy.io/selection-process/candidate/application/{id_candidatura}/step', 
		headers=headers
		)

	info_candidatura = info_candidatura.json()

	teste = pegar_info_teste(info_candidatura, info_candidatura['currentStepId'])

	info_candidatura = {
		'id': info_candidatura['currentStepId'],
		'nome': teste['name'],
		'descricao': teste['objectivesDescription']

	}

	return info_candidatura

def pegar_info_teste(info_candidatura, id_teste_atual):
	for teste in info_candidatura['job']['jobSteps']:
		if teste['id'] == id_teste_atual:
			return teste