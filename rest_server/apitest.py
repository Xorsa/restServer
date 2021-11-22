from os import name, path
from api1 import Api


from fpdf import FPDF

_api = Api('127.0.0.1', 1488)  # инициализируем класс для работы с REST API

d = _api.post(id = 1, name  = 'lols' , size = 1) #Загрузка нового pdf файла
# pdf = _api.get(name = 'lols')  #получение файла
# _api.delete(name = 'lols')