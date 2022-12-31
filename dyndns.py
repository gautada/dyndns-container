#!/usr/bin/env python3

"""dyndns_service.py: A rolled up interface to the dynamic dns service, this handles all plugins and configuration handling"""

__author__  = "Adam T. Gautier"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Adam Gautier"
__email__ = "adam@gautier.org"
__status__ = "Development"

from dyndns_plugin import DynDNSPlugin, DynDNSException, DynDNSPluginException, dyndnslog
from hover_plugin import HoverPlugin
import datetime
import os
import argparse
import hashlib
import requests
import json
import time
import logging
import sys
import yaml


class DynDNS(object):
    CURRENT_IP_URL = "https://api.ipify.org"
    INVALID_IP_ADDRESS = "0.0.0.0"
    CACHE_TIMEOUT = 60
    
    def __init__(self, config="/etc/container/dyndns.yml"):
        assert config is not None, "Configuration file must be provided"
        self.__config = None
        with open(config, "r") as file:
            data = file.read()
            self.__config = yaml.safe_load(data)
        assert self.__config is not None, "Configuration not parsed"
        self.__ip = DynDNS.INVALID_IP_ADDRESS
        self.__ip_timestamp = 0
        self.__plugins = {}
        for _config in self.__config['plugins']:
            assert 'name' in _config, "No name provided in plugin configuration"
            if "hover" == _config['name']:
                assert 'username' in _config, "No username provided in plugin configuration"
                assert 'password' in _config, "No password provided in plugin configuration"
                self.__plugins[_config['name']] = {'config':_config, 'plugin':HoverPlugin(_config['username'], _config['password'])}
        
    def __fetch_ip(self):
        ip = self.__ip
        now = datetime.datetime.now().timestamp()

        if DynDNS.CACHE_TIMEOUT <= now - self.__ip_timestamp:
            dyndnslog.warning("Updating IP from external service")
            try:
                response = requests.get(DynDNS.CURRENT_IP_URL)
                if response.ok:
                    ip = response.text
                    self.__ip_timestamp = now
                else:
                    msg = "Invalid HTTP response code[url:%s code:%s] %s" % (response.url, response.status_code, response.text)
                    dyndnslog.error(msg)
                    raise DynDNSException(msg)
            except Exception as e1:
                msg = "EXCEPTION %s %s" % (type(e1), e1)
                dyndnslog.error(msg)
                raise DynDNSException(msg)
        return ip
    
    @property
    def ip(self):
        ip_new = self.__fetch_ip()
        response = {"previous": self.__ip, "current": ip_new, "last": self.__ip_timestamp}
        self.__ip = ip_new
        return response
            
    def record(self, plugin, domain, record_type, name, content=None):
        assert plugin is not None, "plugin cannot be nil."
        assert domain is not None, "domain cannot be nil."
        assert record_type is not None, "record type cannot be nil."
        assert name is not None, "name cannot be nil."
        dyndnslog.info("RECORD: plugin:%s type:%s domain:%s name:%s content:%s" % (plugin, record_type, domain, name, content is not None))
        if plugin not in self.__plugins:
            raise DynDNSPluginException("Plugin(%s) not found" % plugin)
        _plugin = self.__plugins[plugin]
        return _plugin['plugin'].record(domain=domain, record_type=record_type, name=name, content=content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dynamic DNS Service with plugin support.')
    parser.add_argument('--config', default=None, help='Path to configuration file')
    args = parser.parse_args()

    dyndns = DynDNS(args.config)
    host = dyndns.record(plugin='hover', domain='gautier.org', record_type='A', name='psql', content=dyndns.ip['current'])
    print(host)
    
    # iqgGk7BVsd6Kt_knLt-mXhwlTIlYWcMBn9_pD3fAVU8
    val = "INVALID: %s" % datetime.datetime.now()
    field = dyndns.record(plugin='hover', domain='gautier.org', record_type='TXT', name='_acme-challenge.msql', content=val)
    print(field)
