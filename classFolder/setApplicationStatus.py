from classFolder.contacter import Contacter
import json

class SetApplicationStatus():
    def __init__(self, saksnummer, status):
        self.saksnummer = saksnummer
        self.status = status
        self.contacter = Contacter()

    def set_application_status(self):
        res = self.contacter.set_application_status(self.saksnummer, self.status)
        return res