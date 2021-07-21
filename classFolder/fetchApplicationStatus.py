from classFolder.contacter import Contacter
import json

class FetchApplicationStatus():
    def __init__(self, saksnummer):
        self.saksnummer = saksnummer
        self.contacter = Contacter()

    def fetch_application_status_from_expose_user(self):
        res = self.contacter.fetch_application_status(self.saksnummer)
        return res