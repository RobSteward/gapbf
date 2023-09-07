import yaml
from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    config_file_path: str
    grid_size: int
    path_min_length: int
    path_max_length: int
    path_prefix: str
    path_suffix: str
    excluded_nodes: List[str]
    attempt_delay: float
    test_path: str
    stdout_normal: str
    stdout_success: str
    stdout_error: str
    log_file_path: str

    def __init__(self, config_file_path: str) -> None:
        """
        Constructor for Config class
        """
        try:
            with open(config_file_path, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            raise ValueError(f"Configuration file not found: {config_file_path}")
        except yaml.YAMLError:
            raise ValueError(f"Invalid YAML format in configuration file: {config_file_path}")
    

    @classmethod
    def load_config(cls, config_file_path: str) -> 'Config':
        config = cls.load_config_file(config_file_path)
        return cls(
            config_file_path=config_file_path,
            grid_size=config['config']['grid_size'],
            path_min_length=config['config']['path_min_length'],
            path_max_length=config['config']['path_max_length'],
            path_prefix=config['config']['path_prefix'],
            path_suffix=config['config']['path_suffix'],
            excluded_nodes=config['config']['excluded_nodes'],
            attempt_delay=config['config']['attempt_delay'],
            test_path=config['config']['test_path'],
            stdout_normal=config['config']['outputstrings']['stdout_normal'],
            stdout_success=config['config']['outputstrings']['stdout_success'],
            stdout_error=config['config']['outputstrings']['stdout_error'],
            log_file_path=config['config']['log_file_path']
        )     

    def __repr__(self) -> str:
        return f"Config({self.config})"