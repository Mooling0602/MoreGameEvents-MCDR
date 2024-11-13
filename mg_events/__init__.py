import events.death

from mcdreforged.api.all import *

from mg_events.config import check_config, load_config, rawLangPath

def on_load(server: PluginServerInterface, prev_module):
    load_config()
    check_config()

def on_info(server: PluginServerInterface, info: Info):
    if info.is_from_server:
        events.death(rawLangPath)