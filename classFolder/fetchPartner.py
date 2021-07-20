from werkzeug.exceptions import BadRequest
from classFolder.contacter import Contacter
import json

class FetchPartner:
    def __init__(self) -> None:
        pass

    def get_partner(self, personidentifikator: str):
        # Getting the person that requests children from folkeregisteret
        person_requesting_partner = self._get_folkreg_data(personidentifikator)
        if "familierelasjon" not in person_requesting_partner:
            raise BadRequest

        partner_from_freg = self._get_partner_from_freg(person_requesting_partner)
        
        partner = {}
        partner["navn"] = partner_from_freg["navn"]
        partner["identifikasjonsnummer"] = partner_from_freg["identifikasjonsnummer"]        
        
        return partner

    def _get_folkreg_data(self, personidentifikator):
        return json.loads(Contacter().get_folkreg_data(personidentifikator))

    def _get_partner_from_freg(self, person_requesting_partner):
        relations = person_requesting_partner["familierelasjon"]
        
        # Adding all children to the related_children dict
        for i in range(len(relations)):
            if relations[i]["relatertPersonsRolle"] == "ektefelleEllerPartner":
                return self._get_folkreg_data(relations[i]["relatertPerson"])
        