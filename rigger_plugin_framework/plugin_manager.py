# -*- coding:utf-8

from rigger_singleton.singleton import singleton
from rigger_plugin_framework.plugin_collector import PluginCollector
from rigger_plugin_framework.plugin import Plugin
from rigger_plugin_framework.plugin_installer import PluginInstaller


@singleton
class PluginManager:
    __slots__ = (
        "__raw_plugins",
        "__plugin_instances",
        "__plugin_type_map"
    )

    @staticmethod
    def register(cls):
        manager = PluginManager()
        manager.register_plugin(cls)

    @staticmethod
    def raw_plugins():
        """
        获取所有的插件类型(原型)
        :return:
        """
        manager = PluginManager()
        return manager.all_raw_plugins

    @staticmethod
    def plugins():
        """
        获取所有的插件实例
        :return:
        """
        manager = PluginManager()
        return manager.all_plugins

    @staticmethod
    def get_plugin_names_by_type(t):
        plugins = PluginManager().get_plugins_by_type(t)
        ret = []
        for plugin in plugins:
            name = plugin.get_plugin_name()
            ret.append(name)

        return ret

    @staticmethod
    def start_plugins():
        manager = PluginManager()
        manager.launch_plugins()

    @staticmethod
    def pick_plugins(plugin_type, plugin_name=None):
        manager = PluginManager()
        return manager.get_plugins_by_type(plugin_type, plugin_name)

    @staticmethod
    def install(file_path, dest_dir):
        """
        安装指定的插件包
        :param file_path:
        :param dest_dir:
        :return:
        """
        PluginInstaller().install(file_path, dest_dir)

    @staticmethod
    def collect(path):
        """
        发现项目中的插件
        :param path:
        :return:
        """
        PluginCollector.collect(path)

    @staticmethod
    def remove_plugins():
        """

        :return:
        """
        manager = PluginManager()
        manager.__plugin_instances = []
        manager.__plugin_type_map = dict()
        manager.__raw_plugins = []

    def __init__(self):
        self.__raw_plugins = []
        self.__plugin_instances = []
        self.__plugin_type_map = dict()

    def register_plugin(self, cls):
        """
        注册插件
        :param cls:
        :return:
        """
        if cls not in self.__raw_plugins:
            self.__raw_plugins.append(cls)

    def launch_plugins(self):
        """
        启动所有插件
        :return:
        """
        insts = self.__plugin_instances
        if len(insts) <= 0:
            for plugin_cls in self.raw_plugins():
                inst = plugin_cls()
                insts.append(inst)
                inst.on_start()
                self.add_plugin_type(inst)

    def stop_plugins(self):
        """
        停止所有插件
        :return:
        """

        insts = self.__plugin_instances
        for inst in insts:
            assert isinstance(inst, Plugin)
            inst.on_stop()

        self.__plugin_instances = []

        for inst in insts:
            assert isinstance(inst, Plugin)
            inst.on_start()

    def add_plugin_type(self, plugin):
        """
        将插件加入类型映射
        :param plugin:
        :return:
        """
        plugins = self.get_plugins_by_type(plugin.get_plugin_type())
        assert isinstance(plugins, list)
        if plugin not in plugins:
            plugins.append(plugin)

    def get_plugins_by_type(self, plugin_type, plugin_name=None):
        """
        获取指定类型的插件实例列表
        :param plugin_type:
        :param plugin_name:
        :return:
        """
        plugin_types = self.__plugin_type_map.get(plugin_type)
        if plugin_types is None:
            self.__plugin_type_map[plugin_type] = []
            return self.__plugin_type_map.get(plugin_type)
        else:
            if plugin_name is not None:
                temp = []
                for plugin in plugin_types:
                    if plugin.get_plugin_name() == plugin_name:
                        temp.append(plugin)
                return temp
            else:
                return plugin_types

    @property
    def all_raw_plugins(self):
        return self.__raw_plugins

    @property
    def all_plugins(self):
        return self.__plugin_instances

