import os
import mg_events.data.config as cfg
import mg_events.data.runtime as rt

from mcdreforged.api.all import *
from mg_events.utils import extract_file
from .lang import load_lang, lang_manager


class LangConfigFormat(Serializable):
    raw: str = os.path.join("config", "mg_events", "en_us.json")
    others: list = [os.path.join("config", "mg_events", "zh_cn.json")]

class DefaultConfig(Serializable):
    lang_file: LangConfigFormat = LangConfigFormat()
    use_json5: bool = False
    use_unsafe_mcdr_api_to_load_faster: bool = True
    death_keys_extralist: list[str] = ["command.kill.success.single"]
    set_advancement_color_in_content_raw: bool = True

def load_config(server: PluginServerInterface):
    raw_lang_loaded = False
    cfg.plugin_config = server.load_config_simple(file_name='config.yml', target_class=DefaultConfig)
    raw_lang_path =  cfg.plugin_config.lang_file.raw
    if os.path.exists(raw_lang_path):
        load_lang(server, raw_lang_path)
        raw_lang_loaded = True
    else:
        server.logger.error("Unable to load raw lang file, trying to extract from resources.")
        for i in ["en_us.json", "zh_cn.json"]:
            extract_file(server, os.path.join("resources", i), os.path.join(rt.mcdr["plugin"]["config_dir"], i))
    if not os.path.exists(raw_lang_path):
        raise ValueError(f'Invalid lang file ({raw_lang_path}) may configured, plz check your config.')
    if not raw_lang_loaded:
        load_lang(server, raw_lang_path)
    lang_manager(server)