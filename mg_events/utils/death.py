import re
import copy
from mcdreforged.api.all import *

psi = ServerInterface.psi()

def generate_template(lang):
    lang_copy = copy.deepcopy(lang)
    to_delete = []
    for key, value in lang_copy.items():
        if key.startswith("death."):
            value: str
            value = generate_pattern(value)
            lang_copy[key] = value
        else:
            to_delete.append(key)
    for key in to_delete:
        del lang_copy[key]
    return lang_copy

def generate_pattern(format_string):
    # pattern = re.escape(format_string)
    # 替换 %1$s、%2$s 和 %3$s 为对应的捕获组
    replacements = {
        r"%1$s": r"(?P<player>.\w+|\w+)",  # 匹配玩家名
        r"%2$s": r"(?P<killer>.\w+|\w+)",  # 匹配杀手名
        r"%3$s": r"(?P<weapon>\[[^\]]+\])"  # 匹配武器
    }
    for placeholder, regex in replacements.items():
        format_string = format_string.replace(placeholder, regex)
    return f"^{format_string}$"

def parse(template, message):
    death_data = {
        "key": None,
        "player": None,
        "killer": None,
        "weapon": None
    }
    for key, value in template.items():
        pattern = re.compile(value)
        match = pattern.match(message)
        if match:
            death_data['key'] = key
            death_data.update(match.groupdict())
            return death_data
