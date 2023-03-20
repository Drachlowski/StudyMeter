from calendar import c
from enum import IntFlag
from msilib import Table
from flask_login import UserMixin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

db = SQLAlchemy()

VAR_CHAR_LENGTH = 256


class TableColumns:

    @staticmethod
    def var_char_256 (**kwargs):
        return db.Column(sa.VARCHAR(256), **kwargs)

    @staticmethod
    def id_as_primary ():
        return db.Column(sa.INTEGER, primary_key = True)
    
    @staticmethod
    def timestamp ():
        return db.Column(sa.TIMESTAMP)



class Lehrer (UserMixin, db.Model):

    __tablename__   = 'tbl_lehrer'
    id              = TableColumns.id_as_primary()
    benutzername    = TableColumns.var_char_256(unique = True, nullable = False)
    passwort        = TableColumns.var_char_256(unique = True, nullable = False)
    email           = TableColumns.var_char_256(unique = True, nullable = False)


class Termine (db.Model):

    __tablename__ = 'tbl_termine'
    id          = TableColumns.id_as_primary()
    name        = TableColumns.var_char_256(nullable = False)
    zeitstempel = TableColumns.timestamp(nullable = False)
    lehrer      = db.Column(sa.INTEGER, db.ForeignKey('tbl_lehrer.id'), nullable = False)
    kursname    = TableColumns.var_char_256()


class Einladungen (db.Model):

    __tablename__ = 'tbl_einladungen'
    id = TableColumns.id_as_primary()
    termin = db.Column(sa.INTEGER, db.ForeignKey('tbl_termine.id'))


class Teilnehmer (db.Model):

    __tablename__ = 'tbl_teilnehmer'
    id = TableColumns.id_as_primary()
    name = TableColumns.var_char_256(nullable = False)
    termin = db.Column(sa.INTEGER, db.ForeignKey('tbl_termine.id'))


class Fragen (db.Model):
    id = TableColumns.id_as_primary()







login_manager = LoginManager()
@login_manager.user_loader

def load_user (type : str, value : int):
    if type == 'teacher':
        return Lehrer.query.get(int(value))
    return Teilnehmer.query.get(int(value))