from flask import jsonify
from datetime import date
import json
from werkzeug.exceptions import BadRequest
import requests
import copy



class Application():
    def __init__(self, incoming_application_data):
        if not isinstance(incoming_application_data, dict):
            raise BadRequest
        self.application_data = copy.deepcopy(incoming_application_data)

        self.saksnummer = self.application_data['saksnummer'] if 'saksnummer' in self.application_data else None
        self.status = self.application_data['status'] if 'status' in self.application_data else None
        self.identifikasjonsnummer = self.application_data['identifikasjonsnummer']
        self.navn = self.application_data['navn'] if 'navn' in self.application_data else None
        self.barn_barnehage = self.application_data['opplysninger_om_barn_barnehage']
        self.barn_SFO = self.application_data['opplysninger_om_barn_SFO']
        self.sivilstand = self.application_data['sivilstand']
        self.bostedsadresse = self.application_data['bostedsadresse'] if 'bostedsadresse' in self.application_data else None
        self.preferert_kontaktadresse = self.application_data['preferertKontaktadresse'] if 'preferertKontaktadresse' in self.application_data else None
        self.foedsel = self.application_data['foedsel'] if 'foedsel' in self.application_data else None
        self.postadresse = self.application_data['postadresse'] if 'postadresse' in self.application_data else None
        self.samlet_inntekt = self.application_data['samlet_inntekt'] if 'samlet_inntekt' in self.application_data else None
        self.gratis_kjernetid = self.application_data['gratis_kjernetid'] if 'gratis_kjernetid' in self.application_data else None
        self.maks_aarlig_bhg_kostnad = self.application_data['maks_aarlig_bhg_kostnad'] if 'maks_aarlig_bhg_kostnad' in self.application_data else None
        self.flagg = self.application_data['flagg'] if 'flagg' in self.application_data else None
        self.foreldreansvar = self.application_data['foreldreansvar'] if 'foreldreansvar' in self.application_data else None
        self.familierelasjon = self.application_data['familierelasjon'] if 'familierelasjon' in self.application_data else None
        self.requires_manual_processing = False

        if "status_historikk" not in self.application_data:
            self.status_historikk = []
        else:
            self.status_historikk = self.application_data["status_historikk"]

    #Sjekker flagg i søknad, dersom noen flagg er true
    #må søknaden mest sannsynlig behandles manuelt
    def is_ordinary(self):
        for key, value in self.flagg.items():
            if value:
                self.requires_manual_processing = True
                return False
        return True

    #sjekker om vedkommende har samboer
    #TODO Check if this is necessary for non-automatic applications.
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
        self.foedsel = folkreg_data['foedsel']

    def export_as_json(self):
        return json.dumps({
            "saksnummer": self.saksnummer,
            "status": self.status,
            "identifikasjonsnummer": self.identifikasjonsnummer,
            "navn": self.navn,
            "barn_barnehage": self.barn_barnehage,
            "barn_SFO": self.barn_SFO,
            "sivilstand": self.sivilstand,
            "bostedsadresse": self.bostedsadresse,
            "preferert_kontaktadresse": self.preferert_kontaktadresse,
            "foedsel": self.foedsel,
            "postadresse": self.postadresse,
            "samlet_inntekt": self.samlet_inntekt,
            "gratis_kjernetid": self.gratis_kjernetid,
            "maks_aarlig_bhg_kostnad": self.maks_aarlig_bhg_kostnad,
            "flagg": self.flagg,
            "foreldreansvar": self.foreldreansvar,
            "familierelasjon": self.familierelasjon,
            "requires_manual_processing": self. requires_manual_processing,
            "id": "1" #for database
        })

#eksempelbruk av application-metoder
if __name__ == '__main__':
    f = open('application_example.json',)
    application_data = json.load(f)
    f.close()

    app = Application(application_data)
    app.is_ordinary()
    print(app.export_as_json())
    print(app.has_cohabitant())
    print(app.get_cohabitant())