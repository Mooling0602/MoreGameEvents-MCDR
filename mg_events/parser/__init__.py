import mg_events.data.template as template
import mg_events.data.config as cfg

from mcdreforged.api.all import *
from mg_events.utils import get_raw_locale, get_other_locales
from mg_events.event import death as event_death
from mg_events.event import advancement as event_advancement
from . import death, advancement


@new_thread('Loader(mg_events): LoadTemplate')
def load_templates(server: PluginServerInterface):
    raw_locale = get_raw_locale()
    other_locales = get_other_locales()
    template.death[raw_locale] = death.generate_template(cfg.lang.get(raw_locale, None))
    for i in other_locales:
        template.death[i] = death.generate_template(cfg.lang.get(i, None))
    template.advancement[raw_locale] = advancement.generate_format(cfg.lang.get(get_raw_locale(), None))
    for i in other_locales:
        template.advancement[i] = advancement.generate_format(cfg.lang.get(i, None))
    server.logger.info("Templates for parsing are loaded!")

@new_thread('Parser(mg_events): DispathGameEvents')
def parse_content(server: PluginServerInterface, message: str):
    raw_locale = get_raw_locale()
    death_info = death.parse(template.death.get(raw_locale, None), message)
    if death_info is not None:
        event_death.dispatcher(server, death_info, message)
        return
    advancement_info = advancement.parse(template.advancement.get(raw_locale, None), message)
    if advancement_info is not None:
        event_advancement.dispatcher(server, advancement_info, message)
        return
