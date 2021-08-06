from classFolder.contacter import Contacter
import json

class FetchAllApplications:

    def get_applicants_data(self, personidentifikator):
        contacter = Contacter()
        applications = contacter.fetch_all_applications(personidentifikator)
        return applications