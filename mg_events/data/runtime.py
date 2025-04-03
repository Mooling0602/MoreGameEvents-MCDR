import os


load_complete = False # 插件的加载过程可能耗时较长，故将在单独的线程中运行，并在完成时在此处修改标记
mcdr = {
    "config": None,
    "server_dir": None,
    "plugin": {
        "config_dir": None,
        "meta": None,
        "id": None
    }
}