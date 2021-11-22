import time
import json
from api1 import Data
from flask import Flask, request, jsonify, g
from fpdf import FPDF

app = Flask(__name__)
datafile = 'file.json'
data = Data(datafile)


@app.before_request
def before_request():
    '''
    Исполняется перед каждым запросом.
    Здесь мы начинаем замер времени
    '''
    g.start_time = time.time()

@app.after_request
def after_request(response):
    '''
    Исполняется после каждого запроса.
    Здесь мы замеряем затраченное время сохраняем данные в файл
    и передаем запрос
    '''
    print(f"Time used: {time.time() - g.start_time}")
    return response
   
# @app.route('/', methods=['PUT'])
# def put_item():
	
#  	r = json.loads(request.data)
#  	return 

@app.route('/', methods = ['GET'])
def get_item():
	'''
	Запроса на клиента на получения файла с именем: name
	'''
	name_pdf = request.args.get('name')
	if data.get(name_pdf) != False:
		return jsonify(data.get(name_pdf))
	else:
		return 'Error', 404


@app.route('/', methods=['POST'])
def create_item():
	'''
	Созданиее нового pdf файла( необязательно для быстрого(нет)
	Запрашивает в url его id, name, size(доработать, размер относительный)
	Добавляет в файл формата json(доработать)
	'''
	r = json.loads(request.data)
	data.create_file(r.get('name'),int(r.get('size')))
	return jsonify(data.add(r.get('id'),r.get('name'),r.get('size')))

	
@app.route('/', methods = ['DELETE'])
def delete_file():
	name_pdf = request.args.get('name')
	if (data.delete_pdf(name_pdf) != False):
		return jsonify(data.delete_pdf(name_pdf))
	else:
		return 'Error', 404

app.run(host='127.0.0.1', port=1488, debug=True)
