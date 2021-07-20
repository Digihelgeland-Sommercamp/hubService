from classFolder.contacter import Contacter
import json

class FetchApplicant:
    def __init__(self):
        self.contacter = Contacter()


    def get_applicant_data(self, personidentifikator):
        data = json.loads(self.contacter.get_folkreg_data(personidentifikator))
        res = {
            "navn": data['navn'],
            "bostedsadresse": data['bostedsadresse'],
            "sivilstand": data['sivilstand']
        } 
        return res
