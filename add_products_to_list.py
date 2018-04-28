import requests
import pandas as pd
import time
import re

amazon_data = pd.read_csv('amazon_co-ecommerce_sample.csv',encoding = 'utf-8')

product_names = amazon_data['product_name'] 
product_descriptions = amazon_data['description']
product_prices = amazon_data['price']

headers = {'User-Agent': 'Mozilla/5.0'}

def clean(text):
	text_list = [i for i in str(text) if ord(i) < 128]
	text_list = [' '+i+' ' if not i.isalnum() else i for i in text]
	text = ''.join(text_list)

	text = re.sub(' +',' ',text)

	return text

def clean_number(text):
	text_list = [i for i in str(text) if i.isnumeric()]
	text = ''.join(text_list)+' $'
	text = re.sub(' +',' ',text)
	return text

for product_name,product_description,product_price in zip(product_names,product_descriptions,product_prices):
	try:
		payload = {'optype':'add','name':clean(product_name),'price':clean_number(product_price),'description':clean(product_description)}
		print(payload)
		session = requests.Session()
		session.post('http://127.0.0.1:5500/api/products',headers=headers,data=payload)
	except Exception as e: 
		print(e)