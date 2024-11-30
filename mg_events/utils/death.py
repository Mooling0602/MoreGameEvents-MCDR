import re
import copy

def generate_template(lang):
    lang_copy = copy.deepcopy(lang)
    to_delete = []
    for key, value in lang_copy.items():
        if key.startswith("death."):
            value = generate_pattern(value)
            lang_copy[key] = value
        else:
            to_delete.append(key)
    for key in to_delete:
        del lang_copy[key]
    return lang_copy

def generate_pattern(format_string):
    pattern = re.escape(format_string)
    # 替换 %1$s、%2$s 和 %3$s 为对应的捕获组
    replacements = {
        r"%1\$s": r"(?P<player>\w+)",  # 匹配玩家名
        r"%2\$s": r"(?P<killer>\w+)",  # 匹配杀手名
        r"%3\$s": r"(?P<weapon>\[[^\]]+\])"  # 匹配武器
    }
    for placeholder, regex in replacements.items():
        pattern = pattern.replace(placeholder, regex)
    # 添加开头和结尾标记
    return f"^{pattern}$"

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
