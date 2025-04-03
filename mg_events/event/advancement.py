import mg_events.data.config as cfg

from mcdreforged.api.all import *
from mg_events.utils import get_other_locales, get_raw_locale, parse_dict_value, parse_dict_key
from . import *


def dispatcher(server: PluginServerInterface, data: dict, message: str):
    key = data.get('key', None)
    player = data.get('player', None)
    advancement = data.get('advancement', None)
    server.logger.info("Player advancement event detected!")
    # server.dispatch_event(PlayerAdvancementEvent(player, key, advancement), (player, key, advancement))
    content_list = []
    content = AdvancementContent()
    content.locale = get_raw_locale()
    content.raw = message
    content.advancement = advancement
    for i in translator(key, player, advancement):
        content_list.append(i)
    server.dispatch_event(PlayerAdvancementEvent(player, key, content_list), (player, key, content_list))

def translator(key: str, player: str, advancement: str):
    content_list = []
    for i in get_other_locales():
        lang = cfg.lang[i]
        raw_lang = cfg.lang[get_raw_locale()]
        parsed_raw_message = parse_dict_value(lang, key)
        advancement_tr = parse_dict_value(lang, parse_dict_key(raw_lang, advancement))
        advancement_tr_with_color = f"§r§a[{advancement_tr}]§r"
        if cfg.plugin_config.set_advancement_color_in_content_raw:
            advancement_tr = advancement_tr_with_color
        else:
            advancement_tr = f"[{advancement_tr}]"
        message_tr = parsed_raw_message % (player, advancement_tr)
        content = AdvancementContent()
        content.locale = i
        content.raw = message_tr
        content.advancement = f"[{advancement_tr}]"
        content_list.append(content)
    return content_list

