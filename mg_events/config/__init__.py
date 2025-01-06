import os
import re
import json
import mg_events.data as data

from mcdreforged.api.all import *
from ..utils.death import generate_template
from ..utils.advancement import generate_format
from .default import geyser_config, default_config, extra_death_keys

psi = ServerInterface.psi()

MCDRConfig = psi.get_mcdr_config()
serverDir = MCDRConfig["working_directory"]
configDir = psi.get_data_folder()
plgSelf = psi.get_self_metadata()
plgLoaded = False


def extract_file(file_path, target_path):
    with psi.open_bundled_file(file_path) as file_handler:
        with open(target_path, 'wb') as target_file:
            target_file.write(file_handler.read())

# @new_thread(f'ConfigLoader: {plgSelf.id}')
def check_config(server: PluginServerInterface):
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
    death_keys_dict = server.load_config_simple('extra_death_keys.json', extra_death_keys)
    death_keys_extralist = death_keys_dict["extra"]
    data.config = config
    data.death_keys_extralist = death_keys_extralist
    load_config(server)

def load_config(server: PluginServerInterface):
    server.logger.info("Automatically extracting vanilla lang file, patch version: 1.21.1")
    extract_file('lang/en_us.json', f'{configDir}/en_us.json')
    extract_file('lang/zh_cn.json', f'{configDir}/zh_cn.json')
    server.logger.info("将配置中的en_us改为zh_cn，即可使本插件适配输出中文log的服务端。")
    server.logger.info("中文log可能导致其他适配问题，仍不推荐使用。")
    rawLangPath = data.config["raw_lang"]
    data.rawLangPath = rawLangPath
    if os.path.exists(rawLangPath):
        server.logger.info("Lang file exists, loading plugin...")
        langRegion = os.path.splitext(os.path.basename(rawLangPath))[0]
        if not re.match(r'^[a-z]{2}_[a-z]{2}$', langRegion):
            server.logger.info("Lang region invaild!")
            langRegion = None
        data.langRegion
        data.lang = load_json(rawLangPath, data.config["use_json5"])
        data.template_advancement = generate_format(data.lang)
        data.template_death = generate_template(data.lang)
        server.logger.info("Loading plugin finished!")
        data.plgLoaded = True
    else:
        server.logger.error("Lang file not exists! Please prepare for a one and put in the config folder.")
        server.logger.info(f"Plugin config folder is: {configDir}")
        server.unload_plugin(plgSelf.id)

def load_json(file_path, use_json5, encodings=('utf-8', 'gbk')):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                if use_json5:
                    import json5  # type: ignore
                    return json5.load(f)
                else:
                    return json.load(f)
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Failed to decode {file_path} with encodings: {encodings}")