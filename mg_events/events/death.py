from mcdreforged.api.all import *
from ..config import langRegion, template
from ..utils import content
from ..utils.death import parse

class PlayerDeathEvent(PluginEvent):
    def __init__(self, player: str, event: str, content: dict):
        super().__init__('PlayerDeathEvent')
        self.player = player
        self.event = event
        self.content = content

@new_thread('EventListener: death')
def main(server: PluginServerInterface, info: Info):
    death_data = parse(template, info.content)
    if death_data is not None:
        event = death_data.get('key')
        contentInstance = content()
        contentInstance.lang = langRegion
        deathInstance = contentInstance.death()
        player = death_data.get('player')
        killer = death_data.get('killer')
        weapon = death_data.get('weapon')
        deathInstance.killer = killer
        deathInstance.weapon = weapon
        deathInstance.raw = info.content
        contentInstance.death = deathInstance

        eventInstance = PlayerDeathEvent(player, event, contentInstance)
        server.dispatch_event(eventInstance, (player, event, contentInstance))
        # server.logger.info("Dispatching death event...")