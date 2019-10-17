import requests, json
from parsel import Selector

class Scraper:
    houses = []

    def __init__(self, url):
        for i in range(10):
            text = requests.get(url + '?page=' + str(i+1)).text
            sel = Selector(text=text)
            cards = sel.xpath('//div[@class="card-body"]').getall()
            for item in cards:
                properties_json = {}
                properties_json['place'] = Selector(text=item).xpath('//h4[@class="card-title"]//div//text()').get()
                properties_json['price'] = Selector(text=item).xpath('//h5//text()').get()
                properties = Selector(text=item).xpath('//p[@class="card-text"]//text()').getall()
                for prop in properties:
                    splitted = prop.split(':')
                    key = splitted[0].strip()
                    val = splitted[1].strip()
                    properties_json[key] = val
                extras = Selector(text=item).xpath('//small[@class="text-muted"]//text()').getall()
                properties_json['views'] = extras[0]
                properties_json['date'] = extras[1]
                self.houses.append(properties_json)
