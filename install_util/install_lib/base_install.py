from abc import ABC, abstractclassmethod


class InstallBase(ABC):
    def __init__(self, install_steps=None):
        self.install_steps = install_steps

    @abstractclassmethod
    def preinstall_setup(cls):
        pass

    @abstractclassmethod
    def uninstall(cls):
        pass

    @abstractclassmethod
    def install(cls):
        pass

    @abstractclassmethod
    def init(cls):
        pass

    @abstractclassmethod
    def cleanup(cls):
        pass
