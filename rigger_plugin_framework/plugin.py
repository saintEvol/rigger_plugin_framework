# -*- coding:utf-8

class Plugin:
    __slots__ = ()

    @staticmethod
    def get_plugin_type():
        return 0

    @staticmethod
    def get_plugin_name():
        return ""

    @staticmethod
    def doc():
        return "you shoud descript plug's function here"

    def on_enable(self):
        pass

    def on_disable(self):
        pass

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def on_load(self):
        pass

