from app_amazon import app
from flask import Flask
from flask import send_from_directory

print("at view")

@app.route('/', methods=['GET'])
def index():
	print("at home route")
	return send_from_directory('./static', 'index.html')