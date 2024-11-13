import re

from jtl_api import lang_loader # type: ignore
from mcdreforged.api.all import *

psi = ServerInterface.psi()

class GameEventMessage(PluginEvent):
    def __init__(self, player:str, event:str, content: dict):
        super().__init__('GameEventMessage')
        self.player = player
        self.event = event
        self.content = content

class event(str, Serializable):
    def __new__(cls, raw: str):
        instance = str.__new__(cls, raw)
        instance.raw = raw
        return instance

class content(Serializable):
    lang: str
    advancement: str
    class death(Serializable):
        killer: str
        weapon: str

def match_message(event: str, lang_path, content):
    global match_dict
    psi.logger.info(f"Use {lang_path}")
    lang = lang_loader(lang_path)
    for key in lang.keys():
        if key.startswith(f"{event}."):
            if event == "death":
                value = lang.get(key, None)
                if value:
                    value = re.sub(r'%(\d+)\$s', r'(?P<var\1>.+)', value)
                    match_dict[key] = value
                    for key, value in match_dict.items():
                        match = re.fullmatch(value, content)
                        if match:
                            return key, match.groupdict()
            if event == "chat.type.advancement":
                if value:
                    value = re.sub(r'%s', r'(?P<var1>.+)', value)
                    match_dict[key] = value
                    for key, value in match_dict.items():
                        match = re.fullmatch(value, content)
                        if match:
                            return key, match.groupdict()
    return None, None

def match_death(lang_path, content):
    psi.logger.info(f"Match {lang_path}")
    match_message("death", lang_path, content)

def match_advancement(lang_path, content):
    match_message("chat.type.advancement", lang_path, content)