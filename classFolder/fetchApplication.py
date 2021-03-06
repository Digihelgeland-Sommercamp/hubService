from classFolder.contacter import Contacter
import json

class FetchApplication():
    def __init__(self, saksnummer):
        self.saksnummer = saksnummer
        self.contacter = Contacter()

    def fetch_application_from_expose_user(self):
        res = self.contacter.fetch_application(self.saksnummer)
        return res