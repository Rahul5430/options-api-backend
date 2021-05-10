from flask import Flask, request
from flask_restful import Resource, Api
from nsetools import Nse
from nsepython import *
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup
import requests
# from pprint import pprint

app = Flask(__name__)
api = Api(app)

CORS(app)

nse = Nse()

@app.route('/')
def quote():
    return "Hello!"

@app.route('/1')
def temp():
    url = 'https://www.moneycontrol.com/indices/fno/view-option-chain/NIFTY/2021-05-12'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all('table')
    # print(1)
    # print(tables[1])
    return str(tables[1])

class NseData(Resource):
    def get(self, quote):
        return nse.get_index_quote(quote)

class OptionChain(Resource):
    def get(self, id):
        oi_data, ltp, crontime = oi_chain_builder(id.upper())
        return oi_data.to_dict()

api.add_resource(NseData, '/nsedata/<quote>')
api.add_resource(OptionChain, '/option-chain/<id>')

if __name__ == "__main__":
    # app.run(port=5002)
    app.run()