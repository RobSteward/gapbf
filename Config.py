import yaml
from dataclasses import dataclass, field
from typing import List

@dataclass
class Config:
    config_file_path: str = ''
    grid_size: int = 0
    path_min_length: int = 0
    path_max_length: int = 0
    path_prefix: str = ''
    path_suffix: str = ''
    excluded_nodes: List[str] = field(default_factory=list)
    attempt_delay: float = 0.0
    test_path: str = ''
    stdout_normal: str = ''
    stdout_success: str = ''
    stdout_error: str = ''
    paths_log_file_path: str = ''
    process_log_file_path: str = ''
    debug: bool = False
    adb_timeout: int = 30
        
    @classmethod
    def load_config(cls, config_file_path: str) -> 'Config':
        try:
            with open(config_file_path, 'r') as f:
                config_data = yaml.safe_load(f)
        except FileNotFoundError:
            raise ValueError(f"Configuration file not found: {config_file_path}")
        except yaml.YAMLError:
            raise ValueError(f"Invalid YAML format in configuration file: {config_file_path}")

        return cls(
            config_file_path=config_file_path,
            grid_size=config_data.get('grid_size', 0),
            path_min_length=config_data.get('path_min_length', 0),
            path_max_length=config_data.get('path_max_length', 0),
            path_prefix=config_data.get('path_prefix', ''),
            path_suffix=config_data.get('path_suffix', ''),
            excluded_nodes=config_data.get('excluded_nodes', []),
            attempt_delay=config_data.get('attempt_delay', 0.0),
            test_path=config_data.get('test_path', ''),
            stdout_normal=config_data.get('outputstrings', {}).get('stdout_normal', ''),
            stdout_success=config_data.get('outputstrings', {}).get('stdout_success', ''),
            stdout_error=config_data.get('outputstrings', {}).get('stdout_error', ''),
            paths_log_file_path=config_data.get('paths_log_file_path', ''),
            process_log_file_path=config_data.get('process_log_file_path', ''),
            debug=config_data.get('debug', False),
            adb_timeout = config_data.get('adb_timeout', 30)
        )

def __repr__(self) -> str:
    return f"Config({self.config_file_path})"