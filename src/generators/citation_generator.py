from .base import BaseGenerator


class CitationGenerator(BaseGenerator):
    def generate(self):
        author = self.config["contributors"][0]["name"]
        year = self.config["published"].split("-")[0]
        # Create citation key: lastnameyeartitle
        last_name = author.lower().split()[-1]
        title_key = self.config["title"].lower().replace("-", "").replace(" ", "")
        citation_key = f"{last_name}{year}{title_key}"

        # Build HuggingFace URL
        hf_url = f"https://huggingface.co/{self.config['hugging_face']['type']}/{self.config['hugging_face']['repo']}"

        return f"""@dataset{{{citation_key},
  author = {{{author}}},
  title  = {{{self.config['title']}: {self.config['tagline']}}},
  year   = {{{year}}},
  url    = {{{hf_url}}},
  doi    = {{{self.config['doi']}}},
  note   = {{Version {self.config['version']}, {self.config['contributors'][0]['affiliation']}}}
}}"""
