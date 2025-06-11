from jinja2 import Environment, FileSystemLoader
from .base import BaseGenerator


class LicenseGenerator(BaseGenerator):
    def generate(self):
        env = Environment(loader=FileSystemLoader("src/templates/"))
        template = env.get_template("License.md.j2")
        return template.render(**self.config)
