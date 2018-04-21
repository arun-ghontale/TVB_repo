from flask import Flask, send_from_directory, request, Response
from pymongo import MongoClient as pm
from Mongo_client import mongoclient,mongoclient_user
import re


#initializr the server
products_client = mongoclient(27017)
users_client = mongoclient_user(27017)

# client =  pm('localhost',27017)
app = Flask('mini-amazon', static_url_path='')
# DB = client.products



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

        if request.form['optype'] == 'add':
        
            product = dict()
            product['name'] = request.form['name']
            product['description'] = request.form['description']
            product['price'] = request.form['price']

            result = products_client.insert(product)

            # result = DB.products.insert_one(product)
            #print(result)
            if result:
                return Response(str({'Status' : 'Product added'}), mimetype = 'application/json' ,status = 200)
            else:
                return Response(str({'Status' : 'Product addition unsuccessful'}), mimetype = 'application/json' ,status = 500)
        

        elif request.form['optype'] == 'delete':

            del_product = dict()
            del_product['name'] = request.form['name']

            print("\n\n")
            print(del_product)
            print("\n\n")
            result = products_client.delete(del_product)

            # DB.products.delete_one(filter = del_product)
            if result:
                return Response(str({'Status' : 'Product removed'}), mimetype = 'application/json' ,status = 200)

            else:
                return Response(str({'Status' : 'Product not found'}), mimetype = 'application/json' ,status = 404)

        elif request.form['optype'] == 'update':

            update_product = dict()

            name_criteria = request.form['name-criteria']
            if request.form['name'] != '': 
                update_product['name'] = request.form['name']
            
            if request.form['description'] != '':
                update_product['description'] = request.form['description']

            if request.form['price'] != '':
                update_product['price'] = request.form['price']
 
            # DB.products.update_one(filter = {"name": name_criteria},update={"$set": update_product})

            result = products_client.update(name_criteria,update_product)

            # DB.products.delete_one(filter = del_product)
            if result:
                return Response(str({'Status' : 'Product updated'}), mimetype = 'application/json' ,status = 200)

            else:
                return Response(str({'Status' : 'Product not found'}), mimetype = 'application/json' ,status = 404)


    elif request.method == 'GET':
        
        # result = DB.products.find({'name':request.args['name']})
 
        result = products_client.find(request.args['name'])

        match = []
        for product in result:
            match.append(product)
        if not match:
            return Response(str({"Status":"No product"}),mimetype = 'application/json',status = 404)
        

        return Response(str(match),mimetype = 'application/json',status = 200)


@app.route('/api/users', methods=['POST'])
def users():

    user = dict()
    user['name'] = request.form['name']
    user['password'] = request.form['password']

    print(user)
    result = users_client.insert(user)

    # result = DB.products.insert_one(product)
    #print(result)
    if result:
        return Response(str({'Status' : 'User added'}), mimetype = 'application/json' ,status = 200)
    else:
        return Response(str({'Status' : 'User addition unsuccessful'}), mimetype = 'application/json' ,status = 500)
        

@app.route('/api/get_prod')
def get_products():
    prods = [i for i in products_client.dbase.find()]
    return Response(str(prods), mimetype = 'application/json' ,status = 200)

@app.route('/api/get_user')
def get_users():
    users = [i for i in users_client.duser.find()]
    return Response(str(users), mimetype = 'application/json' ,status = 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)