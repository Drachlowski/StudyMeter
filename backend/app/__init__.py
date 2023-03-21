'''
    Author: Andreas Neubauer

    Dieses File stellt die Funktion create_app bereit. Dieses erstellt, initialisiert und liefert eine Objektinstanz für die Flask-App
    zurück.
'''

from flask import Flask, session
from flask_session import Session
import redis

# Erstellung einer Session
sess = Session()

def create_app () -> Flask:

    # Erstellung einer Objekt-Instanz einer Flask-App
    app = Flask(__name__)

    # Konfiguration
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SECRET_KEY'] = 'super secret key'
    app.config['SESSION_REDIS'] = redis.Redis(host='172.17.0.3')

    # Initialisierung der Session
    sess.init_app(app)


    @app.route('/')
    def index (): return 'Done'

    # Initialisierung und Registrierung der API Blaupause
    from .api import api
    app.register_blueprint(api)


    return app
