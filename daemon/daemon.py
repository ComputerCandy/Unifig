#!/usr/bin/env python

import ConfigProviders.ConfigurationProviders
import socket
import os
import configparser
import sys
import logging as log
import threading


def getConfiguration(configFile="../config/daemon.ini"):
    log.info("Loading daemon config at " + configFile)
    config = configparser.ConfigParser()
    config.read(configFile)
    return config


def getConfigurationProvider(config):
    configuationProvider = None
    for section in config.sections():
        if "ConfigProvider:" in section:
            if configuationProvider != None:
                log.warning(
                    "Multiple configuration providers were found, Only selecting the first one.")
                continue
            name = section.split(":")[-1]
            log.info("Loading configuration provider " + name)
            prov = ConfigProviders.ConfigurationProviders.getProvider(name)
            inst = prov(config[section])
            configuationProvider = inst

    if configuationProvider == None:
        raise Exception("No Configuration Provider specified")
        # TODO: Select a better exception for this

    return configuationProvider


def getValueFromConfig(prov, key):
    v = "$" + key
    while v.startswith("$"):
        k = v[1::]
        log.info("Searching for key " + k + " under investigation of " + key)
        v2 = prov.get(k)

        if v == v2:
            # Infinite loop in config, crash daemon..
            log.error("Infinite config loop at " + v)
            return "$ERROR"
        v = v2
    return v


def processCommand(m, prov):
    msg = m.decode("utf-8").strip()
    log.info("Processing command: " + msg)
    cmd = msg[0]
    parameters = msg[1::].split(",")

    log.info("Parameters: " + parameters[0])
    if cmd == "r":
        if len(parameters) == 3:
            prov.register(parameters[0], parameters[1], parameters[2])
            return "OK"
        log.error("Parameter count for r was " +
                  str(len(parameters)) + ", expecting 3")
        return "$ERROR"
    elif cmd == "g":
        return getValueFromConfig(prov, parameters[0])

    log.error("Command was invalid")
    return "$ERROR"


def manageConnection(client, addr, cfg):
    log.info("New client on " + addr)
    prov = getConfigurationProvider(cfg)
    while True:
        # 8kb messages max, should allow for most documentation
        msg = client.recv(1024 * 8)
        r = processCommand(msg, prov)
        client.send(r.encode("utf-8"))
    client.close()


def run(cfg):
    log.info("Creating Socket")
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    log.info("Removing other socket")
    try:
        os.remove(cfg["Unifig"]["SocketPath"])
    except OSError:
        pass
    log.info("Binding Socket to " + cfg["Unifig"]["SocketPath"])

    s.bind(cfg["Unifig"]["SocketPath"])

    s.listen(0)
    while True:
        c, addr = s.accept()
        threading._start_new_thread(manageConnection, (c, addr, cfg))


log.basicConfig(level="DEBUG")
cfg = getConfiguration()  # We could pass a config path, but not YET
run(cfg)
