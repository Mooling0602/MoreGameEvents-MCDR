import re

from mcdreforged.api.all import *
from jtl_api import parseValue # type: ignore
from ..utils import content, match_death
from ..config import langRegion, lang

death_regex = re.compile(r"death.*")
placeholder_regex = re.compile(r"%(\d+)\$s")

class PlayerDeathMessage(PluginEvent):
    def __init__(self, player: str, event: str, content: dict):
        super().__init__('PlayerDeathMessage')
        self.player = player
        self.event = event
        self.content = content

# @new_thread('EventListen: on_player_death')
def main(server: PluginServerInterface, info: Info):
    key, _ = match_death(info.content)
    if key:
        print(_)
        rawFormat = parseValue(lang, key) # type: ignore
        matches_rawFormat = placeholder_regex.findall(rawFormat)
        regex_template = re.escape(rawFormat)
        regex_template = regex_template.replace(r"%1\$s", r"(.+)").replace(r"%2\$s", r"(.+)").replace(r"%3\$s", r"\[(.+)\]|(.+)")
        content_matches = re.match(regex_template, info.content)

        if content_matches:
            placeholder_to_content = {int(matches_rawFormat[i]): content_matches.group(i + 1) for i in range(len(matches_rawFormat))}
                
            player = placeholder_to_content.get(1, None)
            killer = placeholder_to_content.get(2, None)
            weapon = placeholder_to_content.get(3, None)

            event = key

            contentInstance = content()
            contentInstance.lang = langRegion

            deathInstance = contentInstance.death()
            deathInstance.killer = killer
            deathInstance.weapon = weapon
            deathInstance.raw = info.content
            contentInstance.death = deathInstance

            server.logger.info(f"Detected player: {player} death event")
            server.logger.info(f"Parsed message tr key: {event}")
            server.logger.info(f"Parsed message language: {contentInstance.lang}")
            if re.search(r"death.*", event):
                server.logger.info(f"Parsed death message killer: {contentInstance.death.killer}")
                server.logger.info(f"Parsed death message weapon: {contentInstance.death.weapon}")
            eventInstance = PlayerDeathMessage(player, event, contentInstance)
            server.dispatch_event(eventInstance, (player, event, contentInstance))
            server.logger.info("Dispatching death event...")