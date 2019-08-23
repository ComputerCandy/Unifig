from abc import *


class ConfigurationException(Exception):
    pass


class ConfigurationProvider(metaclass=ABCMeta):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def register(self, key, default, description):
        pass

    @abstractmethod
    def __init__(self, config):
        pass

    @property
    @abstractmethod
    def ConfigName():
        pass
