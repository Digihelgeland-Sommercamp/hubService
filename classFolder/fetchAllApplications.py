from classFolder.contacter import Contacter
import json

class FetchAllApplications:

    def get_applications_data(self, personidentifikator):
        contacter = Contacter()
        applications = contacter.fetch_all_applications(personidentifikator)
        return applications