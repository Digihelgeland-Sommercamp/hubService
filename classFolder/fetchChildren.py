from flask import json
from werkzeug.exceptions import BadRequest
from classFolder.contacter import Contacter

class FetchChildren():
    def __init__(self) -> None:
        pass

    def get_related_children(self, personidentifikator):
        person_requesting_children = self._get_folkreg_data(personidentifikator)
        if "familierelasjon" not in person_requesting_children:
            raise BadRequest
        # print(person_requesting_children["familierelasjon"])
        # return{"test": "test"}

        relations = person_requesting_children["familierelasjon"]
        number_of_children = self._get_number_of_children(relations)
        related_children = [dict for x in range(number_of_children)]
        
        child_index = 0
        for i in range(len(relations)):
            if relations[i]["relatertPersonsRolle"] == "barn":
                related_children[child_index] = self._get_child_from_folkreg(relations[i]["relatertPerson"])
                child_index += 1
        
        return related_children

    def _get_number_of_children(self, relations: list):
        number_of_children = 0
        for i in range(len(relations)):
            if relations[i]["relatertPersonsRolle"] == "barn":
                number_of_children += 1

        return number_of_children

    def _get_folkreg_data(self, personidentifikator):
        return json.loads(Contacter().get_folkreg_data(personidentifikator))

    def _get_child_from_folkreg(self, personidentifikator):
        child_from_folkreg = json.loads(Contacter().get_folkreg_data(personidentifikator))

        child = {}
        child["navn"] = child_from_folkreg["navn"]
        
        return child
