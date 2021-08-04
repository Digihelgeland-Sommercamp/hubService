from classFolder.contacter import Contacter
import json

class FetchAllApplications:

    def get_applicants_data(self, personidentifikator):
        applications = Contacter().fetch_all_applications(personidentifikator)
        return applications