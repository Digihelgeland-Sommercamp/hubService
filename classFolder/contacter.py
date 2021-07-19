import requests
from secrets import token_urlsafe
import json

class Contacter():
    def __init__(self):
        self.skatteserviceURL = "http://localhost:5000/"
        self.folkregserviceURL = "http://localhost:8080/"
        self.evaluatorserviceURL = "http://localhost:8000/"

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

