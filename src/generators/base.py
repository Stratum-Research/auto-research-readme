class BaseGenerator:
    def __init__(self, config):
        self.config = config

    def generate(self):
        raise NotImplementedError

    def write_to_file(self, output_path):
        with open("outputs/" + output_path, "w") as f:
            f.write(self.generate())
