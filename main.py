from bs4 import BeautifulSoup
import requests

session = requests.Session()

payload = {
    'email':'', 
    'password':'',
    'subdomain': 'login'
    }

s = session.post("https://private-api.gupy.io/authentication/candidate/account/signin", data=payload)
print(s.content)

headers = {
    'candidate_key': '',
    'origin': 'https://login.gupy.io',
    'refer': 'https://login.gupy.io/',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

s = session.get('https://private-api.gupy.io/authentication/candidate/account/current', headers=headers)

response = s.json()

for careerPage in response['careerPages']:
    domain = careerPage['subdomain']

    headers.update({
        'origin': f'https://{domain}.gupy.io',
        'refer': f'https://{domain}.gupy.io/',
        })

    s = session.get('https://private-api.gupy.io/selection-process/candidate/application', headers=headers)

    print(careerPage['subdomain'], s.content)