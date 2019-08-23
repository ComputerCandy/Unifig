from ConfigProviders.ConfigurationProvider import *


class FileConfigurationProvider(ConfigurationProvider):
    ConfigName = "File"

    def validateConfig(self, c):
        """Validates the config passed to it in __init__"""
        return ("Path" in c) and True  # Add more conditions

    def __init__(self, config):
        if not self.validateConfig(config):
            raise ConfigurationException()

        self.config = config
        with open(self.config["Path"], "a+"):
            # Write the file new if it is
            pass

        # Index the entire file here

    def register(self, key, default, description):
        v = self.get(key)
        if v == None:
            # Register it with the default
            with open(self.config["Path"], "a") as file:
                cnt = [
                    "#",
                    "# Key: " + key,
                    "# Default: " + default,
                    "# " + description,
                    "#",
                    key + " = " + default,
                    ""
                ]
                file.write("\n".join(cnt))

    def get(self, key):
        """Do some file access here"""

        value = None
        with open(self.config["Path"]) as file:
            for line in file:
                if line.startswith("#"):
                    continue
                if key in line:
                    k, v = line.partition("=")[::2]
                    if k.strip() == key:
                        value = v.strip()
        return value
