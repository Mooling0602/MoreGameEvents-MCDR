import json
import os
import mg_events.data.config as cfg

from typing import Callable, Any
from mcdreforged.api.all import *


# Usage: @execute_if(bool | Callable -> bool)
def execute_if(condition: bool | Callable[[], bool]):
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            actual_condition = condition() if callable(condition) else condition
            if actual_condition:
                return func(*args, **kwargs)
            return None
        return wrapper
    return decorator

def if_contains_any(text: str, str_list: list):
    return any(sub in text for sub in str_list)

def load_json(file_path: str, use_json5: bool, encodings=('utf-8', 'gbk')):
    json_loader = json
    if use_json5:
        try:
            import json5 # type: ignore
            json_loader = json5
        except ModuleNotFoundError:
            pass
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return json_loader.load(f)
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Failed to decode {file_path} with encodings: {encodings}")

def parse_dict_value(data: dict, key: str):
    return data.get(key, None)

def parse_dict_key(data: dict, value: str):
    for k, v in data.items():
        if v == value:
            return k
    return None

def get_raw_locale() -> str:
    return os.path.splitext(os.path.basename(cfg.plugin_config.lang_file.raw))[0]

def get_other_locales() -> list:
    result = []
    for i in cfg.plugin_config.lang_file.others:
        result.append(os.path.splitext(os.path.basename(i))[0])
    return result

def extract_file(server: PluginServerInterface, file_path, target_path):
    with server.open_bundled_file(file_path) as file_handler:
        with open(target_path, 'wb') as target_file:
            target_file.write(file_handler.read())