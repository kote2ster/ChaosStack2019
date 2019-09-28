import hug, json, requests
from db import DB

pythonsqlite = 'pythonsqlite.db'

db = DB(pythonsqlite)
db.create_table()

@hug.get()
def groceries(query: hug.types.text, offset: hug.types.number, limit: hug.types.number, rating: hug.types.number):
    import http.client, urllib.request, urllib.parse, urllib.error, base64

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'c7748d0ad5b447feb47c4bff27aadac0',
    }

    params = urllib.parse.urlencode({})

    return_data = {}

    try:
        conn = http.client.HTTPSConnection('dev.tescolabs.com')
        conn.request("GET", "/grocery/products/?query=" + str(query) + "&offset=" + str(offset) + "&limit=" + str(limit) + "&%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        f = open('out.txt', 'w')
        data = json.loads(str(data.decode()))
        f.write(str(data))
        results = data['uk']['ghs']['products']['results']
        for result in results:
            result['id_prod'] = result['id']
            result['description'] = ''
            db.insert_house(result)
        return_data['why'] = data
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return_data['error'] = 'error'
    return return_data
