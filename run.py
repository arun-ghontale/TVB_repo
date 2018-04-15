from flask import Flask, send_from_directory, request, Response
import pandas as pd
from pymongo import MongoClient as pm
import re

client =  pm('localhost',27017)
app = Flask('mini-amazon', static_url_path='')

DB = client.products
# def save_form(product):
#     print('saving...')
#     with open("forms.txt", "a") as myfile:
#         myfile.write(product['name']+'\t'+product['description']+'\t'+product['price']+'\n')

# def load_form():
#     list_prod = []
#     with open("forms.txt") as myfile:
#         for everyline in myfile.read().split('\n'):
#             if len(everyline.split('\t')) == 3:
#                 list_prod.append({'name':everyline.split('\t')[0],'description':everyline.split('\t')[1],'price':everyline.split('\t')[2]})
#     return list_prod

@app.route('/health', methods=['GET'])
def health():
    return 'healthy'


@app.route('/', methods=['GET'])
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/products', methods=['POST', 'GET'])
def products():
    if request.method == 'POST':


        product = dict()
        product['name'] = request.form['name']
        product['description'] = request.form['description']
        product['price'] = request.form['price']

        result = DB.products.insert_one(product)
        print(result)
        return Response('OK', mimetype = 'application/json' ,status = 200)

    elif request.method == 'GET':
        
        result = DB.products.find({'name':request.args['name']})
        
        match = []
        for product in result:
            match.append(product)
        if not match:
            return Response(str({"Status":"No product"}),mimetype = 'application/json',status = 404)
        

        return Response(str(match),mimetype = 'application/json',status = 200)

        

@app.route('/api/get_prod')
def get_products():

    prods = [i for i in DB.products.find()]
    return Response(str(prods), mimetype = 'application/json' ,status = 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
