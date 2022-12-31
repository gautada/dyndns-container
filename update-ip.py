#!/usr/bin/env python3

"""client.py: Plugin to interface with DNS provided for dynamic dns service"""

__author__  = "Adam T. Gautier"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Adam Gautier"
__email__ = "adam@gautier.org"
__status__ = "Development"

import argparse
import sys
import requests
import yaml
import time

from client import DynDNSClient

"""
ALLOWED_PLUGINS = ['hover']




ip = None
try:
    response = requests.request("get", "http://localhost:8080/ip")
    #, data=None, cookies=self.__cookies)
except Exception as e:
    print(e)
    sys.exit(1)

if response.ok:
    data = response.json()
    if "success" == data['status']:
        ip = data['IP']['current']
    else:
        print(data)
        sys.exit(1)
else:
    print(response.status_code, response.text)
    sys.exit(1)
        

    def __call(self, method, resource, data=None):
        self.__last_response = None
        url = (self.__url + "{0}").format(resource)
        dyndnslog.info("HoverPlugin call(%s): %s" % (method, url))
        try:
            self.__last_response = requests.request(method, url, data=data, cookies=self.__cookies)
        except Exception as e:
            msg = e
            if hasattr(e, 'message'):
                msg = e.message
            raise DynDNSPluginException("Exception(%s): %s" % (type(e), msg))
        if self.__last_response.ok:
            body = self.__last_response.json()
            if "succeeded" not in body or body["succeeded"] is not True:
                raise DynDNSPluginException("%s: (%s) %s" % (self.__last_response.url, self.__last_response.status_code, self.__last_response.text))
            return body
        else:
            raise DynDNSPluginException("%s: (%s) %s" % (self.__last_response.url, self.__last_response.status_code, self.__last_response.text))


for conf in config['plugins']:
    if conf['name'] in ALLOWED_PLUGINS:
        plugin = conf['name']
        print( conf['domains'] )
        for domain, hosts in conf['domains'].items():
            for host in hosts:
                print(plugin, domain, host, ip)
                try:
                    data = '{"plugin":"%s", "domain":"%s", "name":"%s", "content":"%s"}' % (plugin, domain, host, ip)
                    response = requests.request("post", "http://localhost:8080/record", data=data, headers={"Content-Type": "application/json"})
                except Exception as e:
                    print(e)
                    sys.exit(1)
                if response.ok:
                    data = response.json()
                    if "success" == data['status']:
                        print(data)
                    else:
                        print(data)
                        sys.exit(1)
                else:
                    print(response.status_code, response.text)
                    sys.exit(1)
                time.sleep(5)
"""


class DynDNSUpdater():
    ALLOWED_PLUGINS = ['hover']
    
    def __init__(self, url, config):
        with open(config, "r") as file:
            data = file.read()
            self.__config = yaml.safe_load(data)
        self.__client = DynDNSClient(url=url)
    
    def update(self):
        ip = self.__client.ip
        for _conf in self.__config['plugins']:
            if _conf['name'] in DynDNSUpdater.ALLOWED_PLUGINS:
                plugin = _conf['name']
                print( _conf['domains'] )
                for domain, hosts in _conf['domains'].items():
                    for host in hosts:
                        print(plugin, domain, host, ip)
                        self.__client.record(plugin=plugin, domain=domain, record_type='A', name=host, content=ip)
                        time.sleep(5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update IP for domains.')
    parser.add_argument('--url', default='http://localhost:8080', help='API endpoint url')
    parser.add_argument('--config', default="/etc/container/dyndns.yml", help='Configuration file')
    args = parser.parse_args()
    updater = DynDNSUpdater(url=args.url, config=args.config)
    updater.update()
