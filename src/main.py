import argparse
from load import load_config
from generators.hf_generator import HFCardGenerator
from generators.zenodo_generator import ZenodoGenerator
from generators.readme_generator import ReadmeGenerator
from generators.citation_generator import CitationGenerator
from generators.license_generator import LicenseGenerator

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)

    HFCardGenerator(config).write_to_file("dataset_card.json")
    ZenodoGenerator(config).write_to_file("metadata.json")
    ReadmeGenerator(config).write_to_file("README.md")
    CitationGenerator(config).write_to_file("citation.bib")
    LicenseGenerator(config).write_to_file("LICENSE.md")
