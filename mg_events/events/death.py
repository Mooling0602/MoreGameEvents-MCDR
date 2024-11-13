import re

from mcdreforged.api.all import *
from jtl_api import * # type: ignore
from ..utils import event, content, match_death, GameEventMessage
from ..config import langRegion

class PlayerDeathMessage(GameEventMessage):
    def __init__(self, player: str, event, content: dict):
        super().__init__('PlayerDeathMessage')
        self.player = player
        self.event = event
        self.content = content

@new_thread('EventListen: on_player_death')
def main(server: PluginServerInterface, info: Info, lang_path):
    key, _ = match_death(lang_path, info.content)
    if key:
        rawFormat = parseValue(lang, key) # type: ignore
        matches_rawFormat = re.compile(r"%(\d+)\$s").findall(rawFormat)
        regex_template = re.escape(rawFormat).replace(r"%1\$s", r"(.+)").replace(r"%2\$s", r"(.+)").replace(r"%3\$s", r"\[(.+)\]|(.+)")
        content_matches = re.match(regex_template, info.content)

        if content_matches:
            placeholder_to_content = {int(matches_rawFormat[i]): content_matches.group(i + 1) for i in range(len(matches_rawFormat))}
                
            player = placeholder_to_content.get(1, None)
            killer = placeholder_to_content.get(2, None)
            weapon = placeholder_to_content.get(3, None)

    eventInstance = event("death")
    eventInstance.raw = key

    contentInstance = content()
    contentInstance.lang = langRegion

    deathInstance = contentInstance.death()
    deathInstance.killer = killer
    deathInstance.weapon = weapon
    deathInstance.raw = info.content
    contentInstance.death = deathInstance

    server.logger.info(f"Parsed player: {player} death event")
    server.logger.info(f"Parsed message kind: {event}")
    server.logger.info(f"Parsed message tr key: {event.raw}")
    server.logger.info(f"Parsed message language: {content.lang}")
    if event == "death":
        server.logger.info(f"Parsed death message killer: {content.death.killer}")
        server.logger.info(f"Parsed death message weapon: {content.death.weapon}")
    eventInstance = PlayerDeathMessage(player, eventInstance, contentInstance)
    server.dispatch_event(eventInstance, (player, eventInstance, contentInstance))
    server.logger.info("Dispatching death event...")