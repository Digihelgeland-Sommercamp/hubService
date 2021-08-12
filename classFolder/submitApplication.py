from classFolder.application import Application
from classFolder.contacter import Contacter
import json


class SubmitApplication():
    def __init__(self, application_data):
        self.application = Application(application_data)
        self.contacter = Contacter()

    def handle_application(self):
        #sjekk om søknaden uansett må behandles manuelt
        if not self.application.is_ordinary():
            res = self.aborted_save_application()
            return res

        #hent folkeregisterdata
        try:
            folkreg_data = self.get_folkreg_data(self.application.get_idnummer())
            self.application.update_folkreg_data(folkreg_data)
        except Exception as e:
            res = self.aborted_save_application()
            return res

        #hent søkers skattemelding
        applicant_skattemelding = None
        try:
            applicant_skattemelding = self.get_skattemelding("2019", self.application.get_idnummer())

        except Exception as e:
            res = self.aborted_save_application()
            return res
        
        #hent samboer sin skattemelding
        cohabitant_skattemelding = None
        if self.application.has_cohabitant():
            try:
                cohabitant_skattemelding = self.get_skattemelding("2019", self.application.get_cohabitant())
            except Exception:
                res = self.aborted_save_application()
                return res

        #summer inntekt
        self.application.samlet_inntekt = self.sum_bruttoinntekt(applicant_skattemelding, cohabitant_skattemelding)
        
        #spør evaluator
        self.evaluate_income(self.application.samlet_inntekt)

        #lagre søknad
        respons = self.save_application()

        return respons

    def save_application(self):
        res = self.contacter.save_application(self.application.export_as_json())
        return res

    def aborted_save_application(self):
        self.application.requires_manual_processing = True
        res = self.contacter.save_application(self.application.export_as_json())
        return res

    def get_skattemelding(self, inntektsaar, personidentifikator):
        return json.loads(self.contacter.get_skattemelding(inntektsaar, personidentifikator))

    def get_folkreg_data(self, personidentifikator):
        return json.loads(self.contacter.get_folkreg_data(personidentifikator))
    
    def sum_bruttoinntekt(self, applicant_skattemelding, cohabitant_skattemelding):
        res = int(applicant_skattemelding["nettoinntekt"]) + int(applicant_skattemelding["svalbardNettoinntekt"])
        if cohabitant_skattemelding is not None:
            res += int(cohabitant_skattemelding["nettoinntekt"]) + int(cohabitant_skattemelding["svalbardNettoinntekt"])
        return res

    def evaluate_income(self, income):
        for i in range(len(self.application.barn_barnehage)):
            birth = self.application.barn_barnehage[i]["foedsel"]
            personid = self.application.barn_barnehage[i]["foedselsnummer"]
            result = json.loads(self.contacter.evaluate_yearly_income(income, birth))
            self.application.barn_barnehage[i]["gratisKjernetid"] = result["freeHours"]
            self.application.barn_barnehage[i]["maks_aarlig_kostnad"] = result["maxPay"]