from rigger_singleton.singleton import singleton
import importlib
import os


class PluginDescriptor:
    __slots__ = (
        "name",
        "path",
        "module"
    )


@singleton
class PluginCollector:
    """
    插件收集器
    发现安装的插件
    """
    __slots__ = (
        "__paths",
    )

    def __init__(self, paths):
        if paths is list:
            self.__paths = paths
        else:
            self.__paths = []

    @staticmethod
    def path_to_package(path):
        assert isinstance(path, str)
        temp_arr = path.split(os.path.sep)
        if len(temp_arr) > 0 and (temp_arr[0] == "." or temp_arr[0] == ".."):
            temp_arr = temp_arr[1:]

        return ".".join(temp_arr)

    @staticmethod
    def collect(path):
        """
        收集已经安装的插件
        收集完成后， 可以通过PluginManager访问所有插件
        :param path:
        :return:
        """
        assert isinstance(path, str)

        if not os.path.isdir(path):
            raise EnvironmentError("is not a directory")

        items = os.listdir(path)
        for item in items:
            # path/plugindir/pluginpkg
            temp_path = os.path.join(path, item)
            if os.path.isdir(temp_path):
                # 检查是否是包
                if os.path.exists(os.path.join(temp_path, "__init__.py")):
                    pkg = PluginCollector.path_to_package(temp_path)
                    print("import path:", pkg)
                    importlib.import_module(pkg)
                else:
                    pass
                # 继续查找下一层目录
                PluginCollector.collect(temp_path)
            else:
                pass



