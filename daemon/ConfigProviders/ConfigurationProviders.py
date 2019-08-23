import ConfigProviders.FileConfigurationProvider
from ConfigProviders.ConfigurationProvider import *


def getProvider(name):
    providers = [
        ConfigProviders.FileConfigurationProvider.FileConfigurationProvider
    ]
    for provider in providers:
        if provider.ConfigName == name:
            return provider

    raise ConfigurationException(
        "The configuration provider \"" + name + "\" was not found")
