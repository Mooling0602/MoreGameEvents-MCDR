from importlib import import_module
from mcdreforged.api.all import *
from .config import check_config

def on_load(server: PluginServerInterface, prev_module):
    check_config(server)
    
def on_info(server: PluginServerInterface, info: Info):
    if info.is_from_server:
        import_event(server, info, "death")
        import_event(server, info, "advancement")

def import_event(server: PluginServerInterface, info: Info, event_kind):
    api_module = import_module(f'mg_events.events.{event_kind}')
    api_module.main(server, info) # type: ignore
