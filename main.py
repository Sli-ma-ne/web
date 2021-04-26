import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image
import pygame as pg
from random import randint

pg.init()
spn = 0
ll = [37.622504, 55.753215]
layer = "map"
object = ""
need_input = False
address_ll = [0, 0]
address = ''
index = ''
org_name = ''

class Button:
    def __init__(self, width, height, inactive_color=(13, 162, 58), active_color=(23, 204, 58)):
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        
    def draw(self, x, y, message=''):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pg.draw.rect(sc, self.active_color, (x, y, self.width, self.height))
            if click[0] == 1:
                return True   
        else:
            pg.draw.rect(sc, self.inactive_color, (x, y, self.width, self.height))
            
        print_text(message, x + 5, y + 5)
        
def print_text(message, x, y, font_color=(0, 0, 0), font_size=26):
    font_type = pg.font.SysFont('arial', font_size)
    text = font_type.render(message, True, font_color)
    sc.blit(text, (x, y))
    
    
def img():
    global spn, ll, layer, object, address_ll, address, index, org_name
    # Собираем параметры для запроса к StaticMapsAPI:
    if object:
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": object,
            "format": "json"}
        
        response = requests.get(geocoder_api_server, params=geocoder_params)
        json_response = response.json()
        address_ll = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()

        ll = list(map(float, address_ll))
        object = ''
        

        
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": f"{ll[0]},{ll[1]}",
            "format": "json"}
        
        response = requests.get(geocoder_api_server, params=geocoder_params)
        json_response = response.json()
        address = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
        try:
            index = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
        except:
            index = 'Индекс не обнаружен!!!'
        
        search_api_server = "https://search-maps.yandex.ru/v1/"
        api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
        
        
        search_params = {
            "apikey": api_key,
            "text": "организация",
            "lang": "ru_RU",
            "ll": f"{address_ll[0]},{address_ll[1]}",
            "type": "biz",
            "spn": "0.0008,0.0008"
        }
        
        response = requests.get(search_api_server, params=search_params)
        try:
            json_response = response.json()
            organization = json_response["features"][0]
            org_name = organization["properties"]["CompanyMetaData"]["name"]
        except:
            org_name = 'не найдено'        
        #print(json_response)
  

        


    map_params = {
        "ll": f"{ll[0]},{ll[1]}",
        "spn": f"{[0.005, 0.01, 0.02, 0.035, 0.045][spn]},{[0.005, 0.01, 0.02, 0.035, 0.045][spn]}",
        "l": layer,
        "pt": f"{address_ll[0]},{address_ll[1]},comma"
    }
        
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    
    return BytesIO(response.content)
    # Создадим картинку
    # и тут же ее покажем встроенным просмотрщиком операционной системы
    
def spn2(x, x1):
    a1 = str((float(x1[0]) - float(x[0])) / 21)
    a2 = str((float(x1[1]) - float(x[1])) / 21)
    a = f'{a1},{a2}'
    return a  


def img2(toponym_to_find):    
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    
    response = requests.get(geocoder_api_server, params=geocoder_params)
    
    if not response:
        # обработка ошибочной ситуации
        pass
    
    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    delta = spn2(toponym['boundedBy']['Envelope']['lowerCorner'].split(), toponym['boundedBy']['Envelope']['upperCorner'].split())
    
    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": delta,
        "l": ["map", "sat"][randint(0, 1)]
    }
    
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    
    return BytesIO(response.content)
    # Создадим картинку
    # и тут же ее покажем встроенным просмотрщиком операционной системы


def slimane():
    logof = pg.image.load('data/logo/logof.png')
    SLIMANE = []
    SLIMANE.append((pg.image.load('data/logo/S.png'), (261, 290)))
    SLIMANE.append((pg.image.load('data/logo/L.png'), (309, 290)))
    SLIMANE.append((pg.image.load('data/logo/I.png'), (357, 290)))
    SLIMANE.append((pg.image.load('data/logo/M.png'), (389, 290)))
    SLIMANE.append((pg.image.load('data/logo/A.png'), (437, 290)))
    SLIMANE.append((pg.image.load('data/logo/N.png'), (485, 290)))
    SLIMANE.append((pg.image.load('data/logo/E.png'), (533, 290)))  
    studios = pg.image.load('data/logo/studios.png')    
    for i in range(851, 253, -8):
        clock.tick(300)
        sc.blit(logof, (245, 274))
        sc.blit(SLIMANE[0][0], (i, 290))
        pg.display.flip()
    for i in range(851, 301, -8):
        clock.tick(300)
        sc.blit(logof, (245, 274))
        sc.blit(*SLIMANE[0])
        sc.blit(SLIMANE[1][0], (i, 290))
        pg.display.flip()
    for i in range(851, 349, -8):
        clock.tick(300)
        sc.blit(logof, (245, 274))
        for j in range(2):
            sc.blit(*SLIMANE[j])
        sc.blit(SLIMANE[2][0], (i, 290))
        pg.display.flip() 
    for i in range(851, 381, -8):
        clock.tick(300)
        sc.blit(logof, (245, 274))
        for j in range(3):
            sc.blit(*SLIMANE[j])
        sc.blit(SLIMANE[3][0], (i, 290))
        pg.display.flip() 
    for i in range(851, 429, -8):
        clock.tick(300)
        sc.blit(logof, (245, 274))
        for j in range(4):
            sc.blit(*SLIMANE[j])
        sc.blit(SLIMANE[4][0], (i, 290))
        pg.display.flip() 
    for i in range(851, 477, -8):
        clock.tick(300)
        sc.blit(logof, (245, 274))
        for j in range(5):
            sc.blit(*SLIMANE[j])
        sc.blit(SLIMANE[5][0], (i, 290))
        pg.display.flip() 
    for i in range(851, 525, -8):
        clock.tick(300)
        sc.blit(logof, (245, 274))
        for j in range(6):
            sc.blit(*SLIMANE[j])
        sc.blit(SLIMANE[6][0], (i, 290))
        pg.display.flip() 
    for i in range(851, 277, -8):
        clock.tick(300)
        sc.blit(logof, (245, 274))
        for j in range(7):
            sc.blit(*SLIMANE[j])
        sc.blit(studios, (i, 354))
        pg.display.flip()
    pg.time.delay(300)   
    
    
def carta():
    global spn, ll, layer, object, address_ll, address, index, org_name, need_input, input_flag, index_flag, input_text, dog_surf

    while 1:
        try:

            sc.fill((255, 255, 255))
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    pg.quit()
                if need_input and i.type == pg.KEYDOWN:
                    #if i.key == pg.K_RETURN:
                        #need_input = False
                        #input_text = ''
                    if i.key == pg.K_BACKSPACE:
                        if input_text:
                            input_text = input_text[:-1]
                            
                    else:
                        input_text += i.unicode
                    
                    
            if pg.mouse.get_pressed()[0]:
                mouse = pg.mouse.get_pos()
                if 50 < mouse[0] < 650 and 50 < mouse[1] < 500:
                    address_ll[0] = ll[0] + (350 - mouse[0]) * [0.005 * -0.0043, 0.01 * -0.0043, 0.02 * -0.0043, 0.035 * -0.005, 0.045 * -0.0077][spn]
                    address_ll[1] = ll[1] + (275 - mouse[1]) * [0.005 * 0.0024, 0.01 * 0.0024, 0.02 * 0.0024, 0.035 * 0.00275, 0.045 * 0.0043][spn]
                    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
                    geocoder_params = {
                        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                        "geocode": f"{address_ll[0]},{address_ll[1]}",
                        "format": "json"}
                    
                    response = requests.get(geocoder_api_server, params=geocoder_params)
                    json_response = response.json()
                    address = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
                    try:
                        index = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
                    except:
                        index = 'Индекс не обнаружен!!!'
                        
                    search_api_server = "https://search-maps.yandex.ru/v1/"
                    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
                    
                    
                    search_params = {
                        "apikey": api_key,
                        "text": "организация",
                        "lang": "ru_RU",
                        "ll": f"{address_ll[0]},{address_ll[1]}",
                        "type": "biz",
                        "spn": "0.0008,0.0008"
                    }
                    
                    response = requests.get(search_api_server, params=search_params)
                    try:
                        json_response = response.json()
                        organization = json_response["features"][0]
                        org_name = organization["properties"]["CompanyMetaData"]["name"]
                    except:
                        org_name = 'не найдено'
                    
                    
                    
                    dog_surf = pg.image.load(img())
                
                clock.tick(3)
                
                
            keys = pg.key.get_pressed()
            if keys[pg.K_PAGEUP]:
                spn = spn - 1 if spn - 1 > 0 else 0 
                #print(spn)
                dog_surf = pg.image.load(img())
                clock.tick(3)
            if keys[pg.K_PAGEDOWN]:
                spn = spn + 1 if spn + 1 < 4 else 4 
                #print(spn)
                dog_surf = pg.image.load(img())
                clock.tick(3)
            if keys[pg.K_UP]:
                ll[1] += [0.005, 0.01, 0.02, 0.035, 0.045][spn]
                dog_surf = pg.image.load(img())
                clock.tick(3)     
            if keys[pg.K_DOWN]:
                ll[1] -= [0.005, 0.01, 0.02, 0.035, 0.045][spn]
                dog_surf = pg.image.load(img())
                clock.tick(3)    
            if keys[pg.K_RIGHT]:
                ll[0] += [0.005, 0.01, 0.02, 0.035, 0.045][spn]
                dog_surf = pg.image.load(img())
                clock.tick(3)     
            if keys[pg.K_LEFT]:
                ll[0] -= [0.005, 0.01, 0.02, 0.035, 0.045][spn]
                dog_surf = pg.image.load(img())
                clock.tick(3)    
            if layer1.draw(700, 50, message='схема'):
                layer = 'map'
                dog_surf = pg.image.load(img())
                
            if layer1.draw(700, 150, message='спутник'):
                layer = 'sat'
                dog_surf = pg.image.load(img())
                
            if layer1.draw(700, 250, message='гибрид'):
                layer = 'sat,skl'
                dog_surf = pg.image.load(img())
    
            
            if input_flag:
                if input_v.draw(50, 550, message='Нажмите, чтобы начать ввод'):
                    input_flag = False
                    need_input = True
                    clock.tick(3)                    
            else:
                if input_v.draw(50, 550, message=input_text):
                    input_text = ''
                    input_flag = True
                    need_input = False   
                    clock.tick(3) 
            
            if layer1.draw(700, 550, message='Искать'):
                input_flag = True
                need_input = False              
                object = input_text
                dog_surf = pg.image.load(img())   
                input_text = ''
                
            if layer1.draw(700, 450, message='Сброс'):
                address_ll = [0, 0]
                object = ""
                address = ''
                index = ''
                org_name = ''
                dog_surf = pg.image.load(img())     
                input_text = ''
                input_flag = True
                need_input = False            
                
            if address:
                print_text(f'адрес: {address}', 50, 620, font_size=20)
                
            if index_flag:
                if layer2.draw(50, 650, message='скрыть индекс'):
                    index_flag = False
                    clock.tick(3) 
            else:
                if layer2.draw(50, 650, message='показывать индекс'):
                    index_flag = True
                    clock.tick(3) 
                    
            if layer1.draw(50, 750, message='Меню'):
                clock.tick(1)
                menu()
                
                
            if index and index_flag:
                print_text(f'индекс: {index}', 270, 650, font_size=20)
                
            print_text(f'организация: {org_name}', 50, 700, font_size=20)
                
            sc.blit(dog_surf, dog_rect)
            
            clock.tick(60)
            pg.display.update()
        except:
            pass

def menu():
    while 1:
        try:

            sc.fill((255, 255, 255))
            sc.blit(fon, (0, 0))
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    pg.quit()
                    
            if igraB.draw(225, 300, message='   Игра на запоминание карт городов'):
                clock.tick(1)
                igra()
            if cartaB.draw(375, 450, message='  Карта'):
                clock.tick(1)
                carta()
            
            
            clock.tick(60)
            pg.display.update()
        except:
            pass
        
def igra():
    sp = ['москва', 'санкт-петербург', 'екатеринбург', 'пермь', 'челябинск', 'новосибирск', 'казань', 'нижний новгород']
    flagigra = True
    verno = False
    neverno = False
    while 1:
        if flagigra:
            knopka1, knopka2, knopka3, knopka4 = '', '', '', ''
            gorod = sp[randint(0, len(sp) - 1)]
            dog = pg.image.load(img2(gorod))
            a = randint(0, 3)
            if a == 0:
                knopka1 = gorod
            if a == 1:
                knopka2 = gorod
            if a == 2:
                knopka3 = gorod
            if a == 3:
                knopka4 = gorod
            if knopka1 == '':
                knopka1 = sp[randint(0, len(sp) - 1)]
                while knopka1 == knopka2 or knopka1 == knopka3 or knopka1 == knopka4:
                    knopka1 = sp[randint(0, len(sp) - 1)]
                    
                    
            if knopka2 == '':
                knopka2 = sp[randint(0, len(sp) - 1)]
                while knopka2 == knopka1 or knopka2 == knopka3 or knopka2 == knopka4:
                    knopka2 = sp[randint(0, len(sp) - 1)] 
                    
            if knopka3 == '':
                knopka3 = sp[randint(0, len(sp) - 1)]
                while knopka3 == knopka1 or knopka3 == knopka2 or knopka3 == knopka4:
                    knopka3 = sp[randint(0, len(sp) - 1)]
                    
            if knopka4 == '':
                knopka4 = sp[randint(0, len(sp) - 1)]
                while knopka4 == knopka1 or knopka4 == knopka2 or knopka4 == knopka3:
                    knopka4 = sp[randint(0, len(sp) - 1)] 
            
            flagigra = False
            
        sc.fill((255, 255, 255))
        for i in pg.event.get():
            if i.type == pg.QUIT:
                pg.quit()
                
        if layer1.draw(50, 750, message='Меню'):
            clock.tick(1)
            menu()     
        sc.blit(dog, dog_rect)
        if knopka.draw(250, 750, message='Следующая карта'):
            knopka1, knopka2, knopka3, knopka4 = '', '', '', ''
            gorod = sp[randint(0, len(sp) - 1)]
            dog = pg.image.load(img2(gorod))
            a = randint(0, 3)
            if a == 0:
                knopka1 = gorod
            if a == 1:
                knopka2 = gorod
            if a == 2:
                knopka3 = gorod
            if a == 3:
                knopka4 = gorod
            if knopka1 == '':
                knopka1 = sp[randint(0, len(sp) - 1)]
                while knopka1 == knopka2 or knopka1 == knopka3 or knopka1 == knopka4:
                    knopka1 = sp[randint(0, len(sp) - 1)]
                    
                    
            if knopka2 == '':
                knopka2 = sp[randint(0, len(sp) - 1)]
                while knopka2 == knopka1 or knopka2 == knopka3 or knopka2 == knopka4:
                    knopka2 = sp[randint(0, len(sp) - 1)] 
                    
            if knopka3 == '':
                knopka3 = sp[randint(0, len(sp) - 1)]
                while knopka3 == knopka1 or knopka3 == knopka2 or knopka3 == knopka4:
                    knopka3 = sp[randint(0, len(sp) - 1)]
                    
            if knopka4 == '':
                knopka4 = sp[randint(0, len(sp) - 1)]
                while knopka4 == knopka1 or knopka4 == knopka2 or knopka4 == knopka3:
                    knopka4 = sp[randint(0, len(sp) - 1)] 
            
        print_text('Какой город на карте?', 50, 500)
        if layer2.draw(50, 550, message=knopka1):
            if a == 0:
                verno = True
                neverno = False
            else:
                verno = False
                neverno = True
        if layer2.draw(300, 550, message=knopka2):
            if a == 1:
                verno = True
                neverno = False
            else:
                verno = False
                neverno = True
        if layer2.draw(50, 625, message=knopka3):
            if a == 2:
                verno = True
                neverno = False
            else:
                verno = False
                neverno = True
        if layer2.draw(300, 625, message=knopka4):
            if a == 3:
                verno = True
                neverno = False
            else:
                verno = False
                neverno = True      
        if verno:
            print_text('Верно', 550, 550)
        if neverno:
            print_text('Вы ошиблись', 550, 550)
        clock.tick(60)
        pg.display.update()
  
    
    
W = 850
H = 800

sc = pg.display.set_mode((W, H))
clock = pg.time.Clock()

slimane()

sc.fill((255, 255, 255))
fon = pg.image.load('data/fon.jpg')
dog_surf = pg.image.load(img())
dog_rect = dog_surf.get_rect(
    bottomright=(650, 500))
sc.blit(dog_surf, dog_rect)
knopka = Button(200, 50)

layer1 = Button(100, 50)

layer2 = Button(200, 50)

input_v = Button(600, 50)

igraB = Button(400, 50)

cartaB = Button(100, 50)

input_text = ''
input_flag = True
index_flag = True

    
menu()