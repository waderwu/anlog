import os

class Plugin:

    def loadPlugins(self):
        plugins = []
        for filename in os.listdir("plugin"):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            pluginName = os.path.splitext(filename)[0]
            plugin = __import__("plugin." + pluginName, fromlist=[pluginName])
            plugins.append(plugin)