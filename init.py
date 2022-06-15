from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pathlib
from sys import platform

class ActiveApp:
    __app : Optional[Flask] = None 
    __db  : Optional[SQLAlchemy] = None 
    __fp  : Optional[str] = None
    @staticmethod
    def production():
        if (ActiveApp.__app is not None):
            raise Exception("App already running")

        # Different paths for each OS
        if platform == "linux" or platform == "linux2":
            ActiveApp.__fp = f'{pathlib.Path().resolve()}\\tmp\\prod.db'
        else:
            ActiveApp.__fp = f'{pathlib.Path().resolve()}/tmp/prod.db'
            
        ActiveApp.__app = Flask(__name__)
        ActiveApp.__app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{ActiveApp.__fp}'
        ActiveApp.__app.config['SECRET_KEY'] = '123456'

        ActiveApp.__db = SQLAlchemy(ActiveApp.__app)

    @staticmethod
    def test():
        if (ActiveApp.__app is not None):
            raise Exception("App already running")
        
        ActiveApp.__fp = f'{pathlib.Path().resolve()}\\tmp\\test.db'
        ActiveApp.__app = Flask(__name__)
        ActiveApp.__app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{ActiveApp.__fp}'
        ActiveApp.__app.config['SECRET_KEY'] = '123456'
        ActiveApp.__db = SQLAlchemy(ActiveApp.__app)
    
    @staticmethod
    def getApp():
        assert(ActiveApp.__app is not None)
        return ActiveApp.__app

    @staticmethod
    def getDB():
        assert(ActiveApp.__db is not None)
        return ActiveApp.__db
    
    @staticmethod
    def getFP():
        assert(ActiveApp.__fp is not None)
        return ActiveApp.__fp