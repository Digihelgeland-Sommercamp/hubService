import unittest
import os, sys
sys.path.insert(1, os.getcwd()) 
from classFolder.application import Application
import json


app_data = """{
    "saksnummer": "23482973",
    "status": "til behandling",
    "status_historikk": [],
    "navn": {},
    "identifikasjonsnummer": {},
    "sivilstand": {
        "gyldighetstidspunkt": "2017-11-20T00:00:00Z",
        "sivilstand": "gift",
        "sivilstandsdato": "2017-11-20",
        "har_samboer": true,
        "samboer_fra_dato": "2018-11-20",
        "relatert_person": "26919398832"
    },
    "bostedsadresse": {},
    "preferertKontaktadresse": {},
    "foedsel": {},
    "postadresse": {},
    "foreldreansvar": [],   
    "opplysninger_om_barn_barnehage": [],
    "opplysninger_om_barn_SFO": [],
    "familierelasjon": [],
    "samlet_inntekt": 1000000.0,
    "gratis_kjernetid": true,
    "maks_aarlig_bhg_kostnad": null,
    "flagg": {}
}"""

app_data = json.loads(app_data)

class ApplicationTest(unittest.TestCase):

    def test_creation(self):
        app = Application(app_data)
        self.assertEqual(app.saksnummer, "23482973")
        self.assertEqual(app.status, "til behandling")

    def test_has_cohabitant(self):
        app = Application(app_data)
        self.assertTrue(app.has_cohabitant())
        app.sivilstand['har_samboer'] = False
        self.assertFalse(app.has_cohabitant())

    def test_get_cohabitant(self):
        app = Application(app_data)
        self.assertEqual(app.get_cohabitant(), "26919398832")
        app.sivilstand['har_samboer'] = False
        app.sivilstand['relatert_person'] = None
        self.assertFalse(app.get_cohabitant())


if __name__ == '__main__':
    unittest.main()