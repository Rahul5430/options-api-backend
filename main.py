from flask import Flask, request, Response
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
    def inner():
        import datetime
        import time
        start_time = time.time()

        # date
        res = []
        def next_weekday(d, weekday):
            days_ahead = weekday - d.weekday()
            if days_ahead <= 0: # Target day already happened this week
                days_ahead += 7
            return d + datetime.timedelta(days_ahead)

        for i in range(0,28,7):
            x = next_weekday(datetime.date.today() + datetime.timedelta(i), 3)
            day = x.strftime("%d")
            month = x.strftime("%b")
            year = x.strftime("%Y")
            # print(day+'-'+month+'-'+year)
            res.append(day+'-'+month+'-'+year)

        import calendar
        from datetime import datetime

        for i in range(4):
            if i == 3:
                month = calendar.monthcalendar(datetime.today().year, 12)
            else:
                month = calendar.monthcalendar(datetime.today().year, datetime.today().month+1+i)
            thrusday = max(month[-1][calendar.THURSDAY], month[-2][calendar.THURSDAY])
            day = str(thrusday)
            if i == 3:
                currentmonth = datetime.strptime(str(12), "%m").strftime("%b")
            else:
                currentmonth = datetime.strptime(str(datetime.today().month+1+i), "%m").strftime("%b")
            year = str(datetime.today().year)
            res.append(day+'-'+currentmonth+'-'+year)

        print(res)
        yield '%s<br/>\n' % res

        # API
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        from pprint import pprint

        # Authorize the API
        scope = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        file_name = 'client_key.json'
        creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
        client = gspread.authorize(creds)

        # Fetch data from sheet
        print("start")
        yield '%s<br/>\n' % "start"

        for i in range(1,9):
            sheet1 = client.open('ISB shareable-'+str(i)).worksheet('ISB OPTION CHAIN - NIFTY')
            print("Opened sheet", i, "NIFTY")
            yield '%s<br/>\n' % ("Opened sheet "+ str(i) + " NIFTY")
            sheet1.update_cell(2, 2, res[i-1])
            print("Updated sheet", i, "NIFTY")
            yield '%s<br/>\n' % ("Updated sheet "+ str(i) + " NIFTY")
            sheet2 = client.open('ISB shareable-'+str(i)).worksheet('ISB OPTION CHAIN - BANK NIFTY')
            print("Opened sheet", i, "BANKNIFTY")
            yield '%s<br/>\n' % ("Opened sheet "+ str(i) + " BANKNIFTY")
            sheet2.update_cell(2, 2, res[i-1])
            print("Updated sheet", i, "BANKNIFTY")
            yield '%s<br/>\n' % ("Updated sheet "+ str(i) + " BANKNIFTY")

        print("done")
        yield '%s<br/>\n' % "done"

        print("--- %s seconds ---" % (time.time() - start_time))
        yield '%s<br/>\n' % (time.time() - start_time)

















    return Response(inner(), mimetype='text/html')

@app.route('/1')
def temp():
    url = 'https://www.moneycontrol.com/indices/fno/view-option-chain/NIFTY/2021-05-12'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all('table')
    # print(1)
    # print(tables[1])
    return str(tables[1])

@app.route('/2')
def temporary():
    url = 'https://www.moneycontrol.com/indices/fno/view-option-chain/NIFTY/2021-05-12'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    oc = soup.find("div", {"id": "optionchn"})
    return str(oc)

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