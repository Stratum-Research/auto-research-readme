from jinja2 import Environment, FileSystemLoader
from .base import BaseGenerator


class ReadmeGenerator(BaseGenerator):
    def generate(self):
        env = Environment(loader=FileSystemLoader("src/templates/"))
        template = env.get_template("readme.md.j2")
        return template.render(**self.config)
