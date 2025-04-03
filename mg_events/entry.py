import online_player_api as opapi # type: ignore
import mg_events.data.config as cfg
import mg_events.data.runtime as rt
import mg_events.data.template as template

from mcdreforged.api.all import *
from mg_events.loader import loader_main
from mg_events.utils import execute_if, if_contains_any, get_raw_locale
from mg_events.parser import load_templates, parse_content


builder = SimpleCommandBuilder()
psi = ServerInterface.psi()

def on_load(server: PluginServerInterface, prev_module):
    loader_main(server)
    builder.register(server)
    event_register(server)
    if cfg.plugin_config.use_unsafe_mcdr_api_to_load_faster:
        server._plugin_manager._PluginManager__update_registry()

def event_register(server: PluginServerInterface):
    server.register_event_listener("PlayerDeathEvent", on_player_death)
    server.register_event_listener("PlayerAdvancementEvent", on_player_advancement)
    server.register_event_listener("mg_events.load_lang_finished", on_load_lang_finished)

@execute_if(lambda: cfg.plugin_config.use_unsafe_mcdr_api_to_load_faster is False)
def on_server_startup(server: PluginServerInterface):
    server.logger.warning("Reloading plugin due to event registration haven't refreshed yet after on_load stage.")
    server.reload_plugin("mg_events")

def on_player_death(server: PluginServerInterface, player: str, event: str, content: list):
    if server.get_mcdr_language() != get_raw_locale():
        for i in content:
            if i.locale == server.get_mcdr_language():
                server.logger.info(i.raw)

def on_player_advancement(server: PluginServerInterface, player: str, event: str, content):
    if server.get_mcdr_language() != get_raw_locale():
        for i in content:
            if i.locale == server.get_mcdr_language():
                server.logger.info(i.raw)

def on_load_lang_finished(server: PluginServerInterface, locale: str):
    if locale == get_raw_locale():
        rt.load_complete = True
        server.logger.info("Template for parsing is generating...")
        load_templates(server)

def is_need_parse(content: str) -> bool:
    players = opapi.online_players
    if players and len(players) != 0:
        return True
    elif if_contains_any(content, players) is True:
        return True
    else:
        return False

@execute_if(lambda: psi.is_server_running() and rt.load_complete is True)
def on_info(server: PluginServerInterface, info: Info):
    if not is_need_parse(info.content):
        return
    parse_content(server, info.content)

@builder.command('!!mg debug lang')
def on_command_debug_lang(src: CommandSource, ctx: CommandContext):
    src.reply("- Lang")
    src.reply(cfg.lang)

@builder.command('!!mg debug template')
def on_command_debug_template(src: CommandSource, ctx: CommandContext):
    src.reply("- Death Template")
    src.reply(template.death)
    src.reply("- Advancement Template")
    src.reply(template.advancement)