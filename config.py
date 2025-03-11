# config.py
import os

class Config:
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_secreta_por_defecto')

    
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'tiendamvc')

