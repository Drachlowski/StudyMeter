'''
    Author: Andreas Neubauer

    Hier sind alle View-Routes als Klassen implementiert (quick and dirty und keine Datenbank benötigt)
'''

from flask import Blueprint, session, request, jsonify
from flask.views import View

# Erstellung der Blaupause
api = Blueprint('api', 'api', url_prefix='/api')

# from .authentication import *
# from .termine import Termine

# Statische Methode, damit wir schönere und standardisierte Responses zurückgeben können
class APIResponse:

    @staticmethod
    def success (**kwargs):
        return jsonify(dict(
            status = "success",
            **kwargs
        )), 200

    @staticmethod
    def bad_request (**kwargs):
        return jsonify(dict(
            status = "bad request",
            **kwargs
        )), 400
    
    @staticmethod
    def forbidden (**kwargs):
        return jsonify(dict(
            status = "bad request",
            **kwargs
        )), 403


# Dictionary, wo die Termine drinn gespeichert werden (kann auch über die API-Requests geändert werden)
DUMMY_TERMINE = {
    "1": {
        "termin": dict(id = 1, name = "Termin A", zeitstempel = '2023-03-15', kursname = "STP", lehrer = 1),
        "einladungen": [dict(id = 2, termin = 1), dict(id = 2, termin = 1)]
    },
    "2": {
        "termin": dict(id = 2, name = "Quantoren", zeitstempel = '2023-03-15', kursname = "LGI", lehrer = 1),
        "einladungen": [dict(id = 3, termin = 2)],
        "fragen": [
            dict(
                id = 1, 
                termin = 2,
                typ = 'Multiple Choice',
                frage = "Wie sieht das Zeichen eines Allquantors aus?",
                antworten = {"A": "∃", "B": "∀", "C": "∑", "D": "Π" },
                korrekt = 'A'
            ),
            dict (id = 2, 
                termin = 2, 
                frage = "Was ist das Ergebnis von Wahr oder Falsch?",
                typ = 'Freitext Feld',
                korrekt = "Wahr"
            )
        ]
    },
    "3": {
        "termin": dict(id = 3, name = "Rekursion", zeitstempel = '2023-03-15', kursname = "ADE", lehrer = 2),
        "einladungen": [dict(id = 4, termin = 3)]
    }
}

# Counter damit wir wissen wo wir in DUMMY_TERMINE sind
COUNTER = 4

# Dictionary, wo die Termine drinn gespeichert werden (kann auch über die API-Requests geändert werden
DUMMY_LEHRER = {
    "1": dict(id = 1, benutzername = 'da_xavier', passwort = 'Porsche911', email = "franz_porsche@franzxavier.at"),
    "2": dict(id = 2, benutzername = 'da_franz', passwort = 'BMWLife', email = "xavier_bmw@franzxavier.at")
}

# Invites
DUMMY_INVITES = {
}



# View Klasse für die Termine
class Termine (View):

    def __init__(self, type : str) -> None:
        self.__TYPE = type


    def compute_get_request (self, **kwargs):

        if self.__TYPE == 'alles':
            OUTPUT = [DUMMY_TERMINE[x]['termin'] for x in DUMMY_TERMINE if DUMMY_TERMINE[x]['termin']["lehrer"] == session['user']['id']]
            return APIResponse.success(value = OUTPUT)

        if self.__TYPE == 'einzeln':
            termin = kwargs['id']
            if termin not in DUMMY_TERMINE or DUMMY_TERMINE[termin]['termin']["lehrer"] != session['user']['id']: 
                return APIResponse.bad_request(message = "Es gibt keinen Termin mit dieser ID")
            return APIResponse.success(value = DUMMY_TERMINE[termin])


    def request_is_valid (self):
        data = request.get_json()
        if "id" not in data or str(data["id"]) not in DUMMY_TERMINE:
            self.validation_result = "Termin ist nicht gueltig!"
            return False

        return True
    
    def create_event (self, **kwargs):

        DATA = request.get_json()

        if "name" not in DATA:
            return APIResponse.bad_request(message = '"name" is missing')

        if "zeitstempel" not in DATA:
            return APIResponse.bad_request(message = '"zeitstempel" is missing')
        
        global COUNTER
        DUMMY_TERMINE[str(COUNTER)] = dict(termin = dict(
            id = COUNTER,
            name = DATA['name'],
            zeitstempel = DATA['zeitstempel'],
            kursname = DATA['kursname'] if "kursname" in DATA else '',
            lehrer = session['user']['id']
        ))

        COUNTER += 1

        return APIResponse.success(message = 'Event has been created')

    def edit_event (self, **kwargs):
        termin = str(kwargs['id'])
        if termin not in DUMMY_TERMINE or DUMMY_TERMINE[termin]['termin']["lehrer"] != session['user']['id']: 
                return APIResponse.bad_request(message = "Es gibt keinen Termin mit dieser ID")
            
        DATA = request.get_json()

        DATA_TO_UPDATE = {}

        if "name" in DATA: DATA_TO_UPDATE['name'] = DATA['name']
        if "zeitstempel" in DATA: DATA_TO_UPDATE['zeitstempel'] = DATA['zeitstempel']
        if "kursname" in DATA: DATA_TO_UPDATE['kursname'] = DATA['kursname']

        for x in DATA_TO_UPDATE:
            DUMMY_TERMINE[termin]["termin"][x] = DATA_TO_UPDATE[x]

        return APIResponse.success(message = 'Termin erfolgreich bearbeitet')

    def dispatch_request(self, **kwargs):

        if "user" not in session: return APIResponse.forbidden(message = 'Please authenticate to proceed!')

        if request.method == 'GET':
            return self.compute_get_request(**kwargs)

        if request.method == 'POST':
            return self.create_event(**kwargs)
            
        if request.method == 'PATCH':
            return self.edit_event(**kwargs)
        if request.method == 'PUT':
            print(DUMMY_TERMINE)
            print("HERE?")
            if not self.request_is_valid(): return APIResponse.bad_request(message = self.validation_result)
            DUMMY_TERMINE["1"]["termin"]["name"] = "Hello"
            print(DUMMY_TERMINE)
            return APIResponse.success()

        raise NotImplementedError()


# View Klasse für Lehrer
class Lehrer (View):

    def __login (self):
        if "user" in session: return APIResponse.bad_request(message = 'You are already authenticated!')
        DATA = request.get_json()

        for key in DUMMY_LEHRER:
            if DUMMY_LEHRER[key]['benutzername'] == DATA['benutzername'] and DUMMY_LEHRER[key]['passwort'] == DATA['passwort']:
                session['user'] = DUMMY_LEHRER[key]

        if "user" not in session: return APIResponse.bad_request(message = 'Wrong username or password!')
        return APIResponse.success(message = 'Authentication successful!')


    def dispatch_request(self):
        print("HERE?")
        if request.method == 'POST': return self.__login()
        return self.__logout()
    
    def __logout (self):
        if "user" not in session: return APIResponse.forbidden(message = 'Please authenticate to proceed!')

        del session['user']
        return APIResponse.success(message = 'Logout successful!')



# Registrierung der View-Klassen
api.add_url_rule('/termine', view_func=Termine.as_view('termine_handler', "alles"), methods=['GET', 'POST'])
api.add_url_rule('/termine/<id>', view_func=Termine.as_view('einzeltermin', "einzeln"), methods=['GET', 'PATCH'])
# api.add_url_rule('/termine', view_func=Termine.as_view('termine_handler', "alles"), methods=['GET', 'POST'])
api.add_url_rule('/login', view_func=Lehrer.as_view('lehrer_login'), methods=['POST'])
api.add_url_rule('/logout', view_func=Lehrer.as_view('lehrer_logout'), methods=['DELETE'])
