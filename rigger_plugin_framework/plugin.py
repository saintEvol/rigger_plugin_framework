from rigger_singleton.singleton import singleton


@singleton
class Plugin:
    __slots__ = ()

    @property
    def plugin_type(self):
        return 0

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

