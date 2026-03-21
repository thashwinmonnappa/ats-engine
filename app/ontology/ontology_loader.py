import json

class OntologyLoader:

    def __init__(self, ontology_path):
        self.ontology_path = ontology_path
        self.ontology = self.load()

    def load(self):

        with open(self.ontology_path, "r") as f:
            data = json.load(f)

        return data