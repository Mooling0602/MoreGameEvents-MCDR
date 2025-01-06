from mcdreforged.api.all import *

psi = ServerInterface.psi()
MCDRConfig = psi.get_mcdr_config()
serverDir = MCDRConfig["working_directory"]
configDir = psi.get_data_folder()


geyser_config = {
    "raw_lang": f"{serverDir}/plugins/Geyser-Spigot/locales/en_us.json",
    "use_json5": False
}

default_config = {
    "raw_lang": f"{configDir}/en_us.json",
    "use_json5": False
}

extra_death_keys = {
    "extra": ["command.kill.success.single"]
}