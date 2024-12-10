from mcdreforged.api.all import *
from ..utils import content
from ..utils.advancement import parse
from ..config import template_advancement, langRegion
class PlayerAdvancementEvent(PluginEvent):
    def __init__(self, player: str, event: str, content: dict):
        super().__init__('PlayerAdvancementEvent')
        self.player = player
        self.event = event
        self.content = content

@new_thread('EventListener: advancement')
def main(server: PluginServerInterface, info: Info):
    advancement_data = parse(template_advancement, info.content)
    if advancement_data is not None:
        event = advancement_data.get('key')
        player = advancement_data.get('player')
        advancement = advancement_data.get('advancement')
        contentInstance = content()
        contentInstance.raw = info.content
        contentInstance.lang = langRegion
        contentInstance.advancement = advancement

        eventInstance = PlayerAdvancementEvent(player, event, contentInstance)
        server.dispatch_event(eventInstance, (player, event, contentInstance))