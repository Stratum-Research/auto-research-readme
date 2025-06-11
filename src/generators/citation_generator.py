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

        # Check if we have both code and dataset DOIs
        github_doi = self.config.get("github_repo_zenodo_doi")
        dataset_doi = self.config.get("dataset_zenodo_doi")

        if github_doi and dataset_doi:
            # Generate dual citations
            code_citation = f"""@software{{{citation_key}code,
  author = {{{author}}},
  title  = {{{self.config['title']}: Code}},
  year   = {{{year}}},
  url    = {{{self.config.get('github_link', '')}}},
  doi    = {{{github_doi}}},
  note   = {{Version {self.config['version']}, {self.config['contributors'][0]['affiliation']}}}
}}"""

            data_citation = f"""@dataset{{{citation_key}data,
  author = {{{author}}},
  title  = {{{self.config['title']}: {self.config['tagline']}}},
  year   = {{{year}}},
  url    = {{{hf_url}}},
  doi    = {{{dataset_doi}}},
  note   = {{Version {self.config['version']}, {self.config['contributors'][0]['affiliation']}}}
}}"""

            return f"{code_citation}\n\n{data_citation}"
        else:
            # Generate single citation with available DOI
            doi = github_doi or dataset_doi or self.config.get("doi", "")
            return f"""@dataset{{{citation_key},
  author = {{{author}}},
  title  = {{{self.config['title']}: {self.config['tagline']}}},
  year   = {{{year}}},
  url    = {{{hf_url}}},
  doi    = {{{doi}}},
  note   = {{Version {self.config['version']}, {self.config['contributors'][0]['affiliation']}}}
}}"""
