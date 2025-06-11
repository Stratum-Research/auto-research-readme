import json
from .base import BaseGenerator


class HFCardGenerator(BaseGenerator):
    def generate(self):
        card = {
            "title": self.config["title"],
            "pretty_name": self.config["tagline"],
            "version": self.config["version"],
            "language": self.config["language"],
            "license": "mit",
            "tags": self.config.get("tags", []),
            "description": self.config["description"],
            "authors": [
                {
                    "name": c["name"],
                    "email": c["email"],
                    "affiliation": c["affiliation"],
                    "orcid": c["orcid"],
                }
                for c in self.config.get("contributors", [])
            ],
        }
        return json.dumps(card, indent=2)
