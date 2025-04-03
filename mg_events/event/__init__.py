from mcdreforged.api.all import *


class EventContent(Serializable):
    locale: str
    raw: str

class DeathContent(EventContent):
    killer: str
    weapon: str

class AdvancementContent(EventContent):
    advancement: str

class PlayerDeathEvent(PluginEvent):
    def __init__(self, player: str, event: str, content: any):
        super().__init__('PlayerDeathEvent')
        self.player = player
        self.event = event
        self.content = content

class PlayerAdvancementEvent(PluginEvent):
    def __init__(self, player: str, event: str, content: any):
        super().__init__('PlayerAdvancementEvent')
        self.player = player
        self.event = event
        self.content = content