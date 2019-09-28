import hug
import threading
from scraper import Scraper
from db import DB
from linregmodel import LinRegModel
import matplotlib.pyplot as plt


url = 'http://ccnet1.tmit.bme.hu:900/'
pythonsqlite = 'pythonsqlite.db'


#db = DB(pythonsqlite)
#db.create_table()
scraper = Scraper(url)
#for house in scraper.houses:
#    db.insert_house(house)
#db.close()

model = LinRegModel(scraper.houses, degree=1)

def disp_model(model):
    plt.plot(model.x, model.y, 'ro')
    plt.xlabel('property [m2]')
    plt.ylabel('price [million]')

    x_vals = []
    y_vals = []
    for x in range(100):
        x_vals.append(x)
        y_vals.append(model.intercept + model.coeffs[0] * x)
    plt.plot(x_vals, y_vals, 'b')

    plt.show()

@hug.get()
def prediction(property: hug.types.number, balcony: hug.types.number, room: hug.types.number, small_room: hug.types.number,):
    #model = LinRegModel(scraper.houses, degree=degree)
    #threading.Thread(target = disp_model, args = (model,)).start()
    house = {}
    house['property'] = property
    house['balcony'] = balcony
    house['room'] = room
    house['small_room'] = small_room
    return {'prediction': model.predict(house)}
