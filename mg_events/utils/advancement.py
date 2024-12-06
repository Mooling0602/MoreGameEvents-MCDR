import re
import copy

def generate_format(lang):
    lang_copy = copy.deepcopy(lang)
    to_delete = []
    for key, value in lang_copy.items():
        if key.startswith("chat.type.advancement"):
            lang_copy[key] = value.replace('%s', r'(.+)')
        else:
            to_delete.append(key)
    for key in to_delete:
        del lang_copy[key]
    return lang_copy

def parse(template, message):
    advancement_data = {
        "key": None,
        "player": None,
        "advancement": None
    }
    for key, value in template.items():
        match = re.fullmatch(value, message)
        if match:
            advancement_data["key"] = key
            advancement_data["player"] = match.group(1)
            advancement_data["advancement"] = match.group(2)
            return advancement_data