import os
import re
import json

from mcdreforged.api.all import *
from .utils.death import generate_template
from .utils.advancement import generate_format

psi = ServerInterface.psi()

MCDRConfig = psi.get_mcdr_config()
serverDir = MCDRConfig["working_directory"]
configDir = psi.get_data_folder()
plgSelf = psi.get_self_metadata()
plgLoaded = False

geyser_config = {
    "raw_lang": f"{serverDir}/plugins/Geyser-Spigot/locales/en_us.json",
    "use_json5": False
}

default_config = {
    "raw_lang": f"{configDir}/en_us.json",
    "use_json5": False
}

def extract_file(file_path, target_path):
    with psi.open_bundled_file(file_path) as file_handler:
        with open(target_path, 'wb') as target_file:
            target_file.write(file_handler.read())

# @new_thread(f'ConfigLoader: {plgSelf.id}')
def check_config(server: PluginServerInterface):
    global config
    server.logger.info("Supported events at present: death, advancement.")
    if os.path.exists(geyser_config["raw_lang"]):
        useGeyserLocales = True
    else:
        useGeyserLocales = False
    if useGeyserLocales:
        server.logger.info("Detected Geyser installation, using locales from it.")
        config = server.load_config_simple('config.json', geyser_config)
    else:
        config = server.load_config_simple('config.json', default_config)
    load_config(server)

def load_config(server: PluginServerInterface):
    global rawLangPath, langRegion, lang, template_advancement, template_death, plgLoaded
    if not os.path.exists(f"{configDir}/en_us.json"):
        server.logger.info("Automatically extracting built-in lang file, region: en_us, ver: 1.21.1")
        extract_file('lang/en_us.json', f'{configDir}/en_us.json')
    rawLangPath = config["raw_lang"]
    if os.path.exists(rawLangPath):
        server.logger.info("Lang file exists, loading plugin...")
        langRegion = os.path.splitext(os.path.basename(rawLangPath))[0]
        if not re.match(r'^[a-z]{2}_[a-z]{2}$', langRegion):
            langRegion = None
        try:
            with open(f'{rawLangPath}', 'r', encoding='utf-8') as f:
                if config["use_json5"]:
                    import json5 # type: ignore
                    lang = json5.load(f)
                else:
                    lang = json.load(f)
        except UnicodeDecodeError:
            with open(f'{rawLangPath}', 'r', encoding='gbk') as f:
                if config["use_json5"]:
                    import json5 # type: ignore
                    lang = json5.load(f)
                else:
                    lang = json.load(f)
        template_advancement = generate_format(lang)
        template_death = generate_template(lang)
        server.logger.info("Loading plugin finished!")
        plgLoaded = True
    else:
        server.logger.error("Lang file not exists! Please prepare for a one and put in the config folder.")
        server.logger.info(f"Plugin config folder is: {configDir}")
        server.unload_plugin(plgSelf.id)
