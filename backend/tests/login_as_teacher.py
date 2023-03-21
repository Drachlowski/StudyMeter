'''
    Author: Andreas Neubauer

    Dieses Skript testet die Authentifizierung eines Benutzers, ob sich dieser Ein und Ausloggen kann und ob Termine erstellt,
    bearbeitet und einzelne Termine abgerufen werden können.
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


print()
print("Login!")
# Input: benutzername, passwort
# Output: status, message
post_request('/api/login', dict(benutzername = 'da_xavier', passwort = 'Porsche911'))

# Output: status, value als array von json objekten
print("Alle Termine abholen:")
get_request('/api/termine')

# Input: /api/termine/<id>
# Output: status, value als json
print('Zeige den LGI Kurs genauer an')
get_request('/api/termine/2')

# Output: status, message
print('Kurs der mir nicht gehört')
get_request('/api/termine/3')

# Input: name, zeitstempel, kursname (optional) 
# Output: status, message
print('LGI Kurs mit Relationen am 24. Dezember 2023 erstellen')
post_request('/api/termine', dict(name = 'Relationen', kursname = 'LGI', zeitstempel = '2023-12-24'))

# Input id von termin zum Einladung erstellen
# Output: status, message
print('Erstelle Einladung zu LGI Kurs mit Relationen am 24. Dezember 2023 erstellen')
post_request('/api/einladungen', dict(termin = 4))

print('Tritt zum LGI Kurs bei')
post_request('/api/beitreten', dict(einladung = 4, name = "Marcel"))

print('STARTE LGI Termin')
post_request('/api/termine/4', dict(action = 'start'))


# Output: status, value als array von json objekten
print("Alle Termine abholen:")
get_request('/api/termine')

# Input: name, zeitstempel, kursname (optional) 
# Output: status, message
print('Ändere namen von LGI Kurs zu Relationen und FUnktionen')
patch_request('/api/termine/4', dict(name = "Relationen und Funktionen"))

# Output: status, value als array von json objekten
print("Neuen LGI Termin abholen:")
get_request('/api/termine/4')

# Output: status, value als array von json objekten
print("Alle Termine abholen:")
get_request('/api/termine')

# Output: status, message
print("Logge mich von aus 'da_xavier'")
delete_request('/api/logout')


