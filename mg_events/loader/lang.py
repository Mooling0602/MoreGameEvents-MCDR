import os
import re
import mg_events.data.config as cfg

from mcdreforged.api.all import *
from mg_events.utils import load_json


@new_thread(f'Loader(mg_events): LoadLang')
def load_lang(server: PluginServerInterface, file_path: str):
    locale = os.path.splitext(os.path.basename(file_path))[0]
    if not re.match(r'^[a-z]{2}_[a-z]{2}$', locale):
        raise ValueError('Lang filename invalid, please use a valid locale instead!')
    cfg.lang[locale] = load_json(file_path, cfg.plugin_config.use_json5)
    server.dispatch_event(LiteralEvent("mg_events.load_lang_finished"), (locale, ))
    server.logger.info(f"Locale {locale} is loaded!")
    
    