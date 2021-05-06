from flask import Flask, request
from flask_restful import Resource, Api
from nsetools import Nse
from nsepython import *
from flask_cors import CORS, cross_origin
# from pprint import pprint

app = Flask(__name__)
api = Api(app)

CORS(app)

nse = Nse()

@app.route('/')
def quote():
    return "Hello!"

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