'''
    Author: Andreas Neubauer

    Dieses Skript testet die Authentifizierung eines Studenten
'''

import requests as r

BASE_URI = 'http://localhost:8000'

SESSION = r.session()
def get_request (URI):
    URL = BASE_URI + URI
    R = SESSION.get(URL)
    print(f'URL: {URL}')
    print(f'Statuscode: {R.status_code}')
    print(f'Ergebnis: {R.json()}\n')

def post_request (URI, JSON):
    URL = BASE_URI + URI
    R = SESSION.post(URL, json = JSON)
    print(f'URL: {URL}')
    print(f'DATA: {JSON}')
    print(f'Statuscode: {R.status_code}')
    print(f'Ergebnis: {R.json()}\n')

def patch_request (URI, JSON):
    URL = BASE_URI + URI
    R = SESSION.patch(URL, json = JSON)
    print(f'URL: {URL}')
    print(f'DATA: {JSON}')
    print(f'Statuscode: {R.status_code}')
    print(f'Ergebnis: {R.json()}\n')

def delete_request (URI):
    URL = BASE_URI + URI
    R = SESSION.delete(URL)
    print(f'URL: {URL}')
    print(f'Statuscode: {R.status_code}')
    print(f'Ergebnis: {R.json()}\n')


print('Tritt zum LGI Kurs bei (als Marcel)')
post_request('/api/beitreten', dict(einladung = 4, name = "Marcel"))

print('Professor muss lauter sprechen!')
post_request('/api/termine/4', dict(action = 'lauter'))

print('Marcel will eine poffeln gehn!')
post_request('/api/termine/4', dict(action = 'poffeln'))