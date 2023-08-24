import yaml

class ConfigHandler:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def get_value(self, key):
        return self.config.get(key)