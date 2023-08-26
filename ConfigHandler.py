import yaml

class ConfigHandler:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.grid_size = self.get_value('config.grid_size')
        self.path_min_length = self.get_value('config.path_min_length')
        self.path_max_length = self.get_value('config.path_max_length')
        self.path_prefix = self.get_value('config.path_prefix')
        self.path_suffix = self.get_value('config.path_suffix')
        self.excluded_nodes = self.get_value('config.excluded_nodes')
        self.attempt_delay = self.get_value('config.attempt_delay')
        self.test_path = self.get_value('config.test_path')
        self.stdout_normal = self.get_value('config.outputstrings.stdout_normal')
        self.stdout_success = self.get_value('config.outputstrings.stdout_success')
        self.stdout_error = self.get_value('config.outputstrings.stdout_error')
        self.log_file_path = self.get_value('config.log_file_path')

    # Load config file
    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            #print("Loaded config:", config)  # Debugging line
            return config

    def get_value(self, key):
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k)
        return value