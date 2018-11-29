

from rigger_plugin_framework.plugin_manager import PluginManager
import os

path = os.path.join("F:\pythonPro\data2code_plugins\excel_loader_plugin\dist\excel_loader_plugin-0.0.1.tar.gz")
to = os.path.join("..", "plugins")
print(path)
PluginManager.install(path, to)
PluginManager.collect(to)
PluginManager.start_plugins()
print(PluginManager.raw_plugins())
print(PluginManager.plugins())
