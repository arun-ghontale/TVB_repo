from flask import Flask

print("at init.py")
# app = Flask('mini-amazon', static_folder='./app_amazon/static')
app = Flask('mini-amazon' ,static_folder = './static',static_url_path = '',template_folder='./template')

from app_amazon import api, view
