from pymongo import MongoClient as pm
import re

class mongoclient(object):
	def __init__(self,port_number):
		self.port_number = port_number
		print("yo")
		self.client =  pm('localhost',self.port_number)
		print("yo")
		self.DB_collection = self.client.database
		self.dbase = self.DB_collection.database

	def insert(self,product):
	    # try:

		self.DB_collection.database.insert_one(product)
		return 1
	    
	    # # except Exception as e:

	    # 	print(e)
	    # 	return None


	def delete(self,del_product):
		# try:
		self.DB_collection.database.delete_one(filter = del_product)
		return 1
		# except Exception as e:
		# 	print(e)
		# 	return None

	def update(self,name_criteria,update_product):
		# try:
		self.DB_collection.database.update_one(filter = {"name": name_criteria},update={"$set": update_product})
		return 1
		# except Exception as e:
		# 	print(e)
		# 	return None

	def find(self,product):
		# try:
		print(product)
		result = self.DB_collection.database.find({'name':re.compile(product, re.IGNORECASE)})

		# result = self.DB_collection.database.find({'name':product})
		return result
		# except Exception as e:
		# 	print(e)
		# 	return None

	def view(self):
		# try:
		result = DB_collection.database.find()
		return result
		# except Exception as e:
		# 	print(e)
		# 	return None


class mongoclient_user(object):
	def __init__(self,port_number):
		self.port_number = port_number
		self.client =  pm('localhost',self.port_number)
		self.DB_collection = self.client.user
		self.duser = self.DB_collection.user

	def insert(self,product):
	    # try:

		self.DB_collection.user.insert_one(product)
		return 1
	    
	    # # except Exception as e:

	    # 	print(e)
	    # 	return None

	def delete(self,del_product):
		# try:
		self.DB_collection.user.delete_one(filter = del_product)
		return 1
		# except Exception as e:
		# 	print(e)
		# 	return None

	def update(self,name_criteria,update_product):
		# try:
		self.DB_collection.user.update_one(filter = {"name": name_criteria},update={"$set": update_product})
		return 1
		# except Exception as e:
		# 	print(e)
		# 	return None

	def find(self,product):
		# try:
		result = self.DB_collection.user.find({'name':product})
		return result
		# except Exception as e:
		# 	print(e)
		# 	return None

	def find_password(self,password):
		# try:
		result = self.DB_collection.user.find({'password':password})
		return result
		# except Exception as e:
		# 	print(e)
		# 	return None