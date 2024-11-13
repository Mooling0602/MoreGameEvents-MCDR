import mg_events.events.death

from mcdreforged.api.all import *

from mg_events.config import check_config, load_config

def on_load(server: PluginServerInterface, prev_module):
    global rawLangPath, langRegion
    load_config(server)
    rawLangPath, langRegion = check_config(server)
    
def on_info(server: PluginServerInterface, info: Info):
    global rawLangPath, langRegion
    if info.is_from_server:
        server.logger.info(f"Send {rawLangPath}")
        mg_events.events.death.main(server, info, rawLangPath, langRegion)