import requests
from secrets import token_urlsafe
import json
from classFolder import config

class Contacter():
    def __init__(self):
        self.skatteserviceURL = config.hostname_skattservice+config.port_skattservice+'/'
        self.folkregserviceURL = config.hostname_fregservice+config.port_fregservice+'/'
        self.evaluatorserviceURL = config.hostname_evaluatorservice+config.port_evaluatorservice+'/'
        self.exposedataserviceURL = config.hostname_exposedataservice+config.port_exposedataservice+'/'

    def get_skattemelding(self, inntektsaar, personidentifikator):
        url = self.skatteserviceURL + "get_skattemelding/" + str(inntektsaar) + "/" + str(personidentifikator)
        
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception('get_skattemelding request response is not 200. Response: ' + str(r))
        return r.text

    def get_folkreg_data(self, personidentifikator):
        r = requests.get(self.folkregserviceURL + "person/" + str(personidentifikator))
        if r.status_code != 200:
            raise Exception('get_folkreg_data request response is not 200. Status code: ' + str(r.status_code) + ', Reason: ' + str(r.reason))
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
        if r.status_code != 200:
            raise Exception("Could not evaluate yearly income. Response: " + str(r))

        return r.text

    def save_application(self, application_json):
        r = requests.post(self.exposedataserviceURL + "applications/submit_application", json=application_json)
        print(r.text)
        return r.text
    
    def fetch_application(self, saksnummer):
        r = requests.get(self.exposedataserviceURL + "applications/" + str(saksnummer))
        return r.text
    
    def fetch_all_applications(self, personidentifikator):
        r = requests.get(self.exposedataserviceURL + "all_applications/" + str(personidentifikator))
        return r.text

    def fetch_application_status(self, saksnummer):
        r = requests.get(self.exposedataserviceURL + "applications/" + str(saksnummer) + "/status")
        return r.text

    def set_application_status(self, saksnummer, status):
        r = requests.post(self.exposedataserviceURL + "applications/" + str(saksnummer) + "/update_status", data=str(status))
        return r.text

    def upload_attachment(self, data):
        files = {}
        counter = 0
        for i in data.keys():
            files[i] = (data[i].filename, data[i].stream.read(), data[i].content_type)
        r = requests.post(self.exposedataserviceURL + "applications/upload_attachment", files=files)
        return r.text
