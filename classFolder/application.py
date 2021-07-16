from flask import jsonify
from datetime import date
import json



class Application():
    def __init__(self, application_data):
        self.saksnummer = application_data['saksnummer']
        self.status = application_data['status']
        self.identifikasjonsnummer = application_data['identifikasjonsnummer']
        self.navn = application_data['navn']
        self.barn_barnehage = application_data['opplysninger_om_barn_barnehage']
        self.barn_SFO = application_data['opplysninger_om_barn_SFO']
        self.sivilstand = application_data['sivilstand']
        self.bostedsadresse = application_data['bostedsadresse']
        self.preferert_kontaktadresse = application_data['preferertKontaktadresse']
        self.foedsel = application_data['foedsel']
        self.postadresse = application_data['postadresse']
        self.samlet_inntekt = application_data['samlet_inntekt']
        self.gratis_kjernetid = application_data['gratis_kjernetid']
        self.maks_aarlig_bhg_kostnad = application_data['maks_aarlig_bhg_kostnad']
        self.flagg = application_data['flagg']
        self.foreldreansvar = application_data['foreldreansvar']
        self.familierelasjon = application_data['familierelasjon']
        self.requires_manual_processing = False

    #Sjekker flagg i søknad, dersom noen flagg er true
    #må søknaden mest sannsynlig behandles manuelt
    def is_ordinary(self):
        for key, value in self.flagg.items():
            if value:
                self.requires_manual_processing = True
                return False
        return True

    #sjekker om vedkommende har samboer
    def has_cohabitant(self):
        if self.sivilstand['har_samboer']:
            dato = date.today().strftime("%Y-%m-%d")
            if dato != self.sivilstand['samboer_fra_dato']:
                return True
        return False


    #henter personidentifikator til samboer oppgitt i søknad
    def get_cohabitant(self):
        if self.sivilstand['har_samboer']:
            return self.sivilstand['relatert_person']
        return False

    def get_idnummer(self):
        return self.identifikasjonsnummer["foedselsEllerDNummer"]

    #oppdaterer attributter relatert til folkeregistrert data
    def update_folkreg_data(self, folkreg_data):
        self.bostedsadresse = folkreg_data['bostedsadresse']
        self.familierelasjon = folkreg_data['familierelasjon']
        self.foreldreansvar = folkreg_data['foreldreansvar']
        self.postadresse = folkreg_data['postadresse']
        self.preferert_kontaktadresse = folkreg_data['preferertKontaktadresse']

    

#eksempelbruk av application-metoder
if __name__ == '__main__':
    f = open('application_example.json',)
    application_data = json.load(f)
    f.close()

    app = Application(application_data)
    app.is_ordinary()
    print(app.has_cohabitant())
    print(app.get_cohabitant())