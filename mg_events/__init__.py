from mcdreforged.api.all import *
from mg_events.config import check_config, plgLoaded

def on_load(server: PluginServerInterface, prev_module):
    check_config(server)
    
def on_info(server: PluginServerInterface, info: Info):
    if info.is_from_server and plgLoaded:
        import mg_events.events.death
        mg_events.events.death.main(server, info)