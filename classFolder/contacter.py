import requests
from secrets import token_urlsafe
import json
from classFolder import config

class Contacter():
    def __init__(self):
        self.skatteserviceURL = config.hostname_skattservice+config.port_skattservice+'/'
        self.folkregserviceURL = config.hostname_fregservice+config.port_fregservice+'/'
        self.evaluatorserviceURL = config.hostname_evaluatorservice+config.port_evaluatorservice+'/'

    def get_skattemelding(self, inntektsaar, personidentifikator):
        r = requests.get(self.skatteserviceURL + "get_skattemelding/" + str(inntektsaar) + "/" + str(personidentifikator))
        if r.status_code != 200:
            raise Exception('get_skattemelding request response is not 200')
        return r.text

    def get_folkreg_data(self, personidentifikator):
        r = requests.get(self.folkregserviceURL + "person/" + str(personidentifikator))
        if r.status_code != 200:
            raise Exception('get_folkreg_data request response is not 200')
        return r.text

    def evaluate_yearly_income(self, income):
        userId = token_urlsafe()
        data = {
            "userId": userId,
            "income": income,
            "incomeType": "Skatt",
            "monthlyIncome": [
            ],
            "household": [
            ]
        }
        r = requests.get(self.evaluatorserviceURL + "evaluate", json=json.dumps(data))
        return r.text

