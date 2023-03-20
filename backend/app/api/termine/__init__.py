from email import message
import json
from flask.views import View
from flask import request, jsonify

from datetime import datetime

DUMMY_TERMIN = [
    dict(id = 1, name = "Termin A", zeitstempel = '2023-03-15', kursname = "STP"),
    dict(id = 2, name = "Rekursion", zeitstempel = '2023-03-15', kursname = "ADE"),
    dict(id = 3, name = "Quantoren", zeitstempel = '2023-03-15', kursname = "LGI")
]


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


DUMMY_TERMINE = {
    "1": {
        "termin": dict(id = 1, name = "Termin A", zeitstempel = '2023-03-15', kursname = "STP"),
        "einladungen": [dict(id = 2, termin = 1), dict(id = 2, termin = 1)]
    },
    "2": {
        "termin": dict(id = 2, name = "Quantoren", zeitstempel = '2023-03-15', kursname = "LGI"),
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
        "termin": dict(id = 3, name = "Rekursion", zeitstempel = '2023-03-15', kursname = "ADE"),
        "einladungen": [dict(id = 4, termin = 3)]
    }
}



class Termine (View):

    def __init__(self, type : str, data : dict = None) -> None:
        self.__TYPE = type
        self.__DATA = data


    def compute_get_request (self, **kwargs):

        if self.__TYPE == 'alles':
            OUTPUT = [DUMMY_TERMINE[x]['termin'] for x in DUMMY_TERMINE]
            return APIResponse.success(value = OUTPUT)

        if self.__TYPE == 'einzeln':
            termin = kwargs['id']
            if termin not in DUMMY_TERMINE: 
                return APIResponse.bad_request(message = "Es gibt keinen Termin mit dieser ID")
            return APIResponse.success(value = DUMMY_TERMINE[termin])


    def request_is_valid (self):
        data = request.get_json()
        if "id" not in data or str(data["id"]) not in DUMMY_TERMINE:
            self.validation_result = "Termin ist nicht gueltig!"
            return False

        return True


    def dispatch_request(self, **kwargs):
        if request.method == 'GET':
            return self.compute_get_request(**kwargs)

        if request.method == 'POST':
            print(DUMMY_TERMINE)
            print("HERE?")
            if not self.request_is_valid(): return APIResponse.bad_request(message = self.validation_result)
            DUMMY_TERMINE["1"]["termin"]["name"] = "Hello"
            print(DUMMY_TERMINE)
            return APIResponse.success()

        raise NotImplementedError()
