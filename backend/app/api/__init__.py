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
TERMINE_COUNTER = 4
EINLADUNGEN_COUNTER = 4
USER_COUNTER = 1

# Dictionary, wo die Termine drinn gespeichert werden (kann auch über die API-Requests geändert werden
DUMMY_LEHRER = {
    "1": dict(id = 1, benutzername = 'da_xavier', passwort = 'Porsche911', email = "franz_porsche@franzxavier.at"),
    "2": dict(id = 2, benutzername = 'da_franz', passwort = 'BMWLife', email = "xavier_bmw@franzxavier.at")
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
        
        global TERMINE_COUNTER
        DUMMY_TERMINE[str(TERMINE_COUNTER)] = dict(termin = dict(
            id = TERMINE_COUNTER,
            name = DATA['name'],
            zeitstempel = DATA['zeitstempel'],
            kursname = DATA['kursname'] if "kursname" in DATA else '',
            lehrer = session['user']['id']
        ))

        TERMINE_COUNTER += 1

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

    def event_action (self, **kwargs):
        termin = str(kwargs['id'])

        if termin not in DUMMY_TERMINE: return APIResponse.bad_request(message = "Es gibt keinen Termin mit dieser ID")
        if "user" in session and DUMMY_TERMINE[termin]['termin']["lehrer"] != session['user']['id']: 
                return APIResponse.bad_request(message = "Es gibt keinen Termin mit dieser ID")
        
        if "termin" in session and session["termin"] != termin: return APIResponse.forbidden(message = "Bitte poste nur in deinem Termin")
        
        user_type = 'teacher' if 'user' in session else 'student'
        user = session['user']['id'] if user_type == 'teacher' else session['student']
        DATA = request.get_json()

        if "actions" not in DUMMY_TERMINE[termin]: DUMMY_TERMINE[termin]['actions'] = []
        from datetime import datetime as dt
        ACTION = dict(zeitstempel = dt.now(), user_type = user_type, user_id = user, action = DATA['action'])
        DUMMY_TERMINE[termin]['actions'].append(ACTION)

        return APIResponse.success()

    def dispatch_request(self, **kwargs):

        if "user" not in session: return APIResponse.forbidden(message = 'Please authenticate to proceed!')

        if request.method == 'GET':
            return self.compute_get_request(**kwargs)

        if request.method == 'POST':
            if self.__TYPE == 'alles': return self.create_event(**kwargs)
            return self.event_action(**kwargs)
            
        if request.method == 'PATCH':
            return self.edit_event(**kwargs)

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



# View Klasse Einladungen
class Einladungen (View):

    def create_invite (self):
        USER_ID = session['user']['id']

        DATA = request.get_json()


        if "termin" not in DATA: 
            return APIResponse.bad_request(message = 'Ungültige Event ID!')

        termin = str(DATA['termin'])
        if termin not in DUMMY_TERMINE or DUMMY_TERMINE[termin]['termin']['lehrer'] != USER_ID:
            return APIResponse.bad_request(message = 'Ungültige Event ID!')
        
        global EINLADUNGEN_COUNTER
        TERMIN = dict(id = EINLADUNGEN_COUNTER, termin = int(termin))
        if "einladungen" not in DUMMY_TERMINE[termin]: DUMMY_TERMINE[termin]['einladungen'] = []
        DUMMY_TERMINE[termin]['einladungen'].append(TERMIN)
        EINLADUNGEN_COUNTER += 1

        return TERMIN['id']

    def __init__(self, type) -> None:
        self.__TYPE = type
        super().__init__()
    

    def compute_join(self):
        DATA = request.get_json()

        if "einladung" not in DATA or "name" not in DATA:
            return APIResponse.bad_request(message = 'Bitte stelle einen Invite Code und einen Namen bereit!')

        TERMIN = 0
        for termin in DUMMY_TERMINE:
            if "einladungen" not in DUMMY_TERMINE[termin]: continue
            for einladung in DUMMY_TERMINE[termin]['einladungen']:
                print(einladung['id'], DATA["einladung"])
                if einladung['id'] == DATA["einladung"]: TERMIN = termin

        if TERMIN == 0: return APIResponse.bad_request(message = 'Einladung ungültig')

        if "user" in session: return APIResponse.bad_request(message = 'Eingeloggte Lehrer können nicht teilnehmen!')

        global USER_COUNTER
        session['termin'] = TERMIN
        session['student'] = USER_COUNTER
        STUDENT = dict(id = USER_COUNTER, name = DATA['name'], termin = int(TERMIN))
        USER_COUNTER += 1
        if "teilnehmer" not in DUMMY_TERMINE[termin]: DUMMY_TERMINE[termin]['teilnehmer'] = []
        DUMMY_TERMINE[termin]['teilnehmer'].append(STUDENT)

        return APIResponse.success(message = 'Erfolgreich beigetreten!')

    
    def dispatch_request(self):

        if self.__TYPE == 'erstellen':
            invite = self.create_invite()

            if not isinstance(invite, int): return invite
            return APIResponse.success(message = 'Einladung wurde erstellt!', invite_id = invite)
        
        else:
            return self.compute_join()


# Registrierung der View-Klassen
api.add_url_rule('/termine', view_func=Termine.as_view('termine_handler', "alles"), methods=['GET', 'POST'])
api.add_url_rule('/termine/<id>', view_func=Termine.as_view('einzeltermin', "einzeln"), methods=['GET', 'POST', 'PATCH'])
api.add_url_rule('/einladungen', view_func=Einladungen.as_view('erstelle_einladung', 'erstellen'), methods=['POST'])
api.add_url_rule('/beitreten', view_func=Einladungen.as_view('einzeleinladungen', "beitreten"), methods=['POST'])
# api.add_url_rule('/termine', view_func=Termine.as_view('termine_handler', "alles"), methods=['GET', 'POST'])
api.add_url_rule('/login', view_func=Lehrer.as_view('lehrer_login'), methods=['POST'])
api.add_url_rule('/logout', view_func=Lehrer.as_view('lehrer_logout'), methods=['DELETE'])
