from flask import Flask
import pathlib

fp = f'{pathlib.Path().resolve()}\\tmp\\test.db'

app : Flask = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{fp}'
app.config['SECRET_KEY'] = '123456'