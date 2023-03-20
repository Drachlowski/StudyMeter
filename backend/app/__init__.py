from flask import Flask
from app.settings import Settings
from pymongo import MongoClient
from flask import session
from flask_session import Session
import redis
# from flask.s

# client = MongoClient(host='172.17.0.3:27017')
sess = Session()

def create_app () -> Flask:
    app = Flask(__name__)
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SECRET_KEY'] = 'super secret key'
    app.config['SESSION_REDIS'] = redis.Redis(host='redis')
    sess = Session()
    sess.init_app(app)
    @app.route('/')
    def index (): return 'Done'


    from .api import api
    app.register_blueprint(api)


    return app
