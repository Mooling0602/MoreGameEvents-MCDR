import re

from mcdreforged.api.all import *
from mg_events.config import lang

psi = ServerInterface.psi()

match_dict = {}

class content(Serializable):
    lang: str
    advancement: str
    class death(Serializable):
        killer: str
        weapon: str

def match_message(event: str, content):
    global match_dict
    for key in lang.keys():
        if key.startswith(f"{event}."):
            if event == "death":
                value = lang.get(key, None)
                if value:
                    value = re.sub(r'%(\d+)\$s', r'(?P<var\1>.+)', value)
                    match_dict[key] = re.compile(value)
                    match = match_dict[key].fullmatch(content)
                    if match:
                        return key, match.groupdict()
            if event == "chat.type.advancement":
                if value:
                    value = re.sub(r'%s', r'(?P<var1>.+)', value)
                    match_dict[key] = re.compile(value)
                    match = match_dict[key].fullmatch(content)
                    if match:
                        return key, match.groupdict()
    return None, None

def match_death(content):
    key, _ = match_message("death", content)
    return key, _

def match_advancement(content):
    key, _ = match_message("chat.type.advancement", content)
    return key, _