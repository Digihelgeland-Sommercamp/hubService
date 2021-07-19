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
            self.aborted_save_application()
            return True

        #hent folkeregisterdata
        try:
            folkreg_data = self.get_folkreg_data(self.application.get_idnummer())
            self.application.update_folkreg_data(folkreg_data)
        except Exception as e:
            self.aborted_save_application()
            raise Exception(e)

        #hent søkers skattemelding
        applicant_skattemelding = None
        try:
            applicant_skattemelding = self.get_skattemelding("2019", self.application.get_idnummer())
            # applicant_skattemelding = self.get_skattemelding("2019", "03839199405")

        except Exception as e:
            self.aborted_save_application()
            raise Exception(e)
        
        #hent samboer sin skattemelding
        cohabitant_skattemelding = None
        if self.application.has_cohabitant():
            try:
                cohabitant_skattemelding = self.get_skattemelding("2019", self.application.get_cohabitant())
            except Exception:
                self.aborted_save_application()
                raise Exception('Obtaining cohabitant skattemelding failed')

        #summer inntekt
        self.application.samlet_inntekt = self.sum_nettoinntekt(applicant_skattemelding, cohabitant_skattemelding)
        
        #spør evaluator
        res = self.evaluate_income(self.application.samlet_inntekt)
        self.application.gratis_kjernetid = res['freeHours']
        self.application.maks_aarlig_bhg_kostnad = res['maxPay']

        #lagre søknad
        self.save_application()

        return True #if successful operation

    def save_application(self):
        #TODO: 
        #Kontakt intern databaseservice, og lagre søknad
        pass

    def aborted_save_application(self):
        #TODO:
        #Sett requires_manual_processing i application til true,
        #lagre søknad i intern database
        pass

    def get_skattemelding(self, inntektsaar, personidentifikator):
        return json.loads(self.contacter.get_skattemelding(inntektsaar, personidentifikator))

    def get_folkreg_data(self, personidentifikator):
        return json.loads(self.contacter.get_folkreg_data(personidentifikator))
    
    def sum_nettoinntekt(self, applicant_skattemelding, cohabitant_skattemelding):
        res = int(applicant_skattemelding["nettoinntekt"]) + int(applicant_skattemelding["svalbardNettoinntekt"])
        if cohabitant_skattemelding is not None:
            res += int(cohabitant_skattemelding["nettoinntekt"]) + int(cohabitant_skattemelding["svalbardNettoinntekt"])
        return res

    def evaluate_income(self, income):
        return json.loads(self.contacter.evaluate_yearly_income(income))





# #eksempelbruk av submitapplication-metoder
# if __name__ == '__main__':
#     f = open('application_example.json',)
#     application_data = json.load(f)
#     f.close()

#     app = SubmitApplication(application_data)
#     print(app.handle_application())
