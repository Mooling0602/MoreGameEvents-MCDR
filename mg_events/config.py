import os
import re

from mcdreforged.api.all import *
from jtl_api import lang_loader # type: ignore

psi = ServerInterface.psi()

MCDRConfig = psi.get_mcdr_config()
serverDir = MCDRConfig["working_directory"]
configDir = psi.get_data_folder()
plgSelf = psi.get_self_metadata()

geyser_config = {
    "raw_lang": f"{serverDir}/plugins/Geyser-Spigot/locales/en_us.json"
}

default_config = {
    "raw_lang": f"{configDir}/en_us.json"
}

@new_thread('ConfigLoader: mg_events')
def check_config(server: PluginServerInterface):
    global config
    server.logger.info("Supported events at present: death, advancement.")
    if os.path.exists(geyser_config["raw_lang"]):
        useGeyserLocales = True
    if useGeyserLocales:
        server.logger.info("Detected Geyser installation, using locales from it.")
        config = server.load_config_simple('config.json', geyser_config)
    else:
        config = server.load_config_simple('config.json', default_config)
    load_config(server)

def load_config(server: PluginServerInterface):
    global rawLangPath, langRegion, lang
    rawLangPath = config["raw_lang"]
    if os.path.exists(rawLangPath):
        server.logger.info("Lang file exists, loading plugin...")
        langRegion = os.path.splitext(os.path.basename(rawLangPath))[0]
        if not re.match(r'^[a-z]{2}_[a-z]{2}$', langRegion):
            langRegion = None
        lang = lang_loader(rawLangPath)
        server.logger.info("Loading plugin finished!")
        server.logger.info(plgSelf.id)
    else:
        server.logger.error("Lang file not exists! Please prepare for a one and put in the config folder.")
        server.logger.info(f"Plugin config folder is: {configDir}")
        server.unload_plugin(plgSelf.id)