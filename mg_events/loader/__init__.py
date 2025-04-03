import os
import mg_events.data.runtime as rt

from mcdreforged.api.all import *
from .config import load_config


def loader_main(server: PluginServerInterface):
    global raw_locale, other_locale
    # 加载运行时环境
    rt.mcdr["config"] = server.get_mcdr_config()
    rt.mcdr["server_dir"] = rt.mcdr["config"]["working_directory"]
    rt.mcdr["plugin"]["config_dir"] = server.get_data_folder()
    plugin_meta = server.get_self_metadata()
    rt.mcdr["plugin"]["meta"] = plugin_meta
    rt.mcdr["plugin"]["id"] = plugin_meta.id
    load_config(server)