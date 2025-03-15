from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"  
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
