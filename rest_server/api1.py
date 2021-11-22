import json
from typing import DefaultDict
import requests
import os
from dataclasses import dataclass
from shutil import copyfile
from fpdf import FPDF
import webbrowser

class Data(): 
  
    def __init__(self, path = None) -> None:
        self.path = 'C:/Python/rest_server/' #Путь к корневой папке (os не работало)
        self.data: dict = json.loads(open('file.json', 'rb').read()) if path in os.listdir() else {}
    def get(self, name: str):
        '''
        Открытие файла, имя берется с GET (доработать, в случае отсутсвия файла)
        '''
        if os.access(str(self.path) +'{}.pdf'.format(str(name)), os.F_OK) == True:
            return webbrowser.open_new(str(self.path) +'{}.pdf'.format(str(name)))
        else:
            return False

    # def update(self,id:str, name:str, size:str):
    #     if id in self.data.keys():
    #            self.data[id] = {
    #                 'name': name,
    #                 'size': int(size)
    #             }
                
    def add(self, id: int, name: str, size: int):
        '''
        Получение данных с url запроса, id, name, size добавление в файла 'file.json'
        необяз(доработка формата id: id {name: name, size: size}) -> более удобное обращение к файлу
        '''
        if id not in self.data.keys():
                self.data[id] = {
                    'id':id,
                    'name': name,
                    'size': int(size)
                }
                with open('file.json','w') as f:
                    f.write(json.dumps(self.data[id]))
                    f.close()
                return self.data[id]
        else:
                return {'error': 'Item with id={} already exists.'.format(str(id))}
    def create_file(self, name: str, size: int):
        '''
        Получение name, size с запроса POST 
        Создания pdf файла по полученным данным 
        Создания файла тестовое(относительная размерность доработать)

        '''
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 14)
        for i in range(1,int(size)*12):
            pdf.cell(200, 10, txt='', ln=1, align="C")
        pdf.output('{}.pdf'.format(name))
        pdf.close()
    def delete_pdf(self, name: str):
        '''
        Удаление pdf файла 
        access проверка на существование
        '''
        if os.access(str(self.path) +'{}.pdf'.format(str(name)), os.F_OK) == True:
            return os.remove(str(self.path) +'{}.pdf'.format(str(name)))
        else:
            return False


class APIResponse:
    '''
    Класс, держащий дату от ответа с АПИ
    '''
    status_code: int  # статус ответа от сервера АПИ
    data: DefaultDict  # дата в JSON
    raw_response: requests.Response  # весь сырой запрос, на всякий случай

    def __init__(self, r: requests.Response) -> None:
        self.status_code = r.status_code
        self.data = r.json() if r.status_code == 200 else {}
        self.raw_response = r

class Api():
    def __init__(self, host: str, port: int) -> None:
        self.address = f'http://{host}:{port}/'  # ендпоинт REST-API, с которым мы работаем
   
    # def put(self, id: int, name: str, size: int) -> APIResponse:
    #     '''
    #     -------
    #     '''
    #     r = requests.put(self.address, json = {'id': id ,'name':name, 'size': size})
    #     print(r.status_code)
    #     return APIResponse(r)
    def post(self,id: int, name: str, size: int) -> APIResponse:
        '''
        Запрос POST
        '''
        r = requests.post(self.address, json ={
            'id': id,
            'name': '{}'.format(name),
            'size': int(size)
            })
        print(r.status_code)
    def get(self, name: str):
        '''
        Запрос GET
        '''
        r = requests.get(self.address, params = {'name':name})
        print(r.status_code)
    def delete(self, name: str):
        r = requests.delete(self.address, params = {'name':name})
        print (r.status_code)


  

# Для ошибок, доработать
class MissingPathException(Exception):

    def __init__(self, message: str) -> None:
        super().__init__(message)