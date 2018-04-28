from flask import Flask, send_from_directory, request, Response, render_template
from app_amazon import app
from models.Mongo_client import mongoclient
from models.Mongo_client import mongoclient_user
import numpy as np
import os
PRODUCT_VIEW_LIMIT = 10
SET_USERS_NUMBER = 10
SET_PRODUCT_NUMBER = 10


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
    #exception for json inputs
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
        
        print("here ")
        # result = DB.products.find({'name':request.args['name']})
        
        #restrict to top 10 results
        result = products_client.find(request.args['name'])

        match = []
        for ind,product in enumerate(result):
            # print(product)
            match.append(product)
            if ind == PRODUCT_VIEW_LIMIT:
                break

        if not match:
            return Response(str({"Status":"No product"}),mimetype = 'application/json',status = 404)

        if request.args['output_type'] == 'html':
            # print(os.getcwd())
            return render_template('./results.html', query = request.args['name'], results = match)        


        return Response(str(match),mimetype = 'application/json',status = 200)


@app.route('/api/users', methods=['POST'])
def users():
    print("At the users")
    if request.form['act'] == 'signup':

        user = dict()
        user['name'] = request.form['name']
        user['password'] = request.form['pass']
        user['email'] = request.form['Email']

        duplicate_users = users_client.find(user['name'])
        duplicate_users_list = [i for i in duplicate_users]

        if duplicate_users_list:
            return render_template('./Users_temp.html', signup_message = "Username or password already exists")

        users_client.insert(user)
        return render_template('./search.html',username = user['name'])

    elif request.form['act'] == 'login':
        user = request.form.get('name',None)
        password = request.form.get('pass',None)

        authenticate_user = [i for i in users_client.find(user)]
        authenticate_password = [i for i in users_client.find_password(password)]
        print(authenticate_user,authenticate_password)
        if authenticate_user and authenticate_password:
            return render_template('./search.html', username = user)

        else:
            return render_template('./Users_temp.html', login_message = "Wrong username or password")
        # result = DB.products.insert_one(product)
        #print(result)
        # if result:
        #     return Response(str({'Status' : 'Signup successful'}), mimetype = 'application/json' ,status = 200)
        # else:
        #     return Response(str({'Status' : 'Signup Unsuccessful'}), mimetype = 'application/json' ,status = 500)
        
    elif request.form['action'] == 'signup':
        print("at users")
        user = dict()
        user['name'] = request.form['name']
        user['password'] = request.form['password']

        user_match = users_client.find(user)

        if user_match:
            return Response(str({'Status' : 'Signup successful'}), mimetype = 'application/json' ,status = 200)
        else:
            return Response(str({'Status' : 'login Unsuccessful'}), mimetype = 'application/json' ,status = 500)


@app.route('/api/get_prod')
def get_products():

    COUNT_PRODS = products_client.dbase.find().count()    
    use_indices = [np.random.randint(COUNT_PRODS) for i in range(0,SET_PRODUCT_NUMBER)]

    prods = []
    for ind,i in enumerate(products_client.dbase.find()):
        if ind in use_indices:
            prods.append(i)

    return Response(str(prods), mimetype = 'application/json' ,status = 200)

@app.route('/api/get_user')
def get_users():

    COUNT_USERS = products_client.duser.find().count()    
    use_indices = [np.random.randint(COUNT_USERS) for i in range(0,SET_USERS_NUMBER)]

    users = []
    for ind,i in enumerate(users_client.duser.find()):
        if ind in use_indices:
            users.append(i)
    return Response(str(users), mimetype = 'application/json' ,status = 200)