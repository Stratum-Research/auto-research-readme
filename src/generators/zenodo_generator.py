import json
from .base import BaseGenerator


class ZenodoGenerator(BaseGenerator):
    def generate(self):
        return json.dumps(
            {
                "upload_type": "dataset",
                "publication_date": self.config["published"],
                "title": self.config["title"],
                "creators": [
                    {
                        "name": f"{c['name'].split()[1]}, {c['name'].split()[0]}",
                        "affiliation": c["affiliation"],
                        "orcid": c["orcid"],
                    }
                    for c in self.config.get("contributors", [])
                ],
                "description": self.config["description"],
                "license": "mit",
                "keywords": self.config.get("tags", []),
                "version": self.config["version"],
            },
            indent=2,
        )
