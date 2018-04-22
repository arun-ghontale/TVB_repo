from flask import Flask, send_from_directory, request, Response, render_template
from app_amazon import app
from models.Mongo_client import mongoclient
from models.Mongo_client import mongoclient_user
import os

print("at api")

# app = Flask('mini-amazon', static_url_path='')

products_client = mongoclient(27017)
users_client = mongoclient_user(27017)

@app.route('/health', methods=['GET'])
def health():
    return 'healthy'

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

        if request.args['output_type'] == 'html':
            print(os.getcwd())
            return render_template('./results.html', query = request.args['name'], results = match)        


        return Response(str(match),mimetype = 'application/json',status = 200)


@app.route('/api/users', methods=['POST'])
def users():
    print("at users")
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