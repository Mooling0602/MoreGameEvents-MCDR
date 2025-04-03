import online_player_api as opapi # type: ignore
import mg_events.data.config as cfg

from mcdreforged.api.all import *
from mg_events.utils import get_raw_locale, get_other_locales, parse_dict_key, parse_dict_value
from . import *

def dispatcher(server: PluginServerInterface, data: dict, message: str):
    key = data.get('key', None)
    player = data.get('player', None)
    server.logger.info("Player death event detected!")
    extra_info = {
        'killer': data.get('killer', None),
        'weapon': data.get('weapon', None)
    }
    content_list = []
    content = DeathContent()
    content.locale = get_raw_locale()
    content.raw = message
    content.killer = data.get('killer', None)
    content.weapon = data.get('weapon', None)
    for i in translator(key, player, content.killer, content.weapon):
        content_list.append(i)
    server.dispatch_event(PlayerDeathEvent(player, key, content_list), (player, key, content_list))
    
def translator(key: str, player: str, killer: str, weapon: str) -> list[DeathContent]:
    content_list = []
    for i in get_other_locales():
        lang = cfg.lang[i]
        raw_lang = cfg.lang[get_raw_locale()]
        parsed_raw_message = parse_dict_value(lang, key)
        message_tr = parsed_raw_message.replace("%1$s", player)
        if killer is not None:
            if killer not in opapi.get_player_list():
                killer_tr = parse_dict_value(lang, parse_dict_key(raw_lang, killer))
                if killer_tr is not None:
                    killer = killer_tr
            message_tr = message_tr.replace("%2$s", killer)
        if weapon is not None:
            message_tr = message_tr.replace("%3$s", weapon)
        content = DeathContent()
        content.locale = i
        content.raw = message_tr
        content.killer = killer
        content.weapon = weapon
        content_list.append(content)
    return content_list