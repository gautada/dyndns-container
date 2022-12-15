#!/usr/bin/env python3

"""client.py: Plugin to interface with DNS provided for dynamic dns service"""

__author__  = "Adam T. Gautier"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Adam Gautier"
__email__ = "adam@gautier.org"
__status__ = "Development"

import sys
import requests
import yaml
import time

ALLOWED_PLUGINS = ['hover']

configfile="/etc/container/dyndns.yml"
config = None
with open(configfile, "r") as file:
    data = file.read()
    config = yaml.safe_load(data)


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
        
"""
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
"""

for conf in config['plugins']:
    if conf['name'] in ALLOWED_PLUGINS:
        plugin = conf['name']
        print( conf['domains'] )
        for domain, hosts in conf['domains'].items():
            for host in hosts:
                print(plugin, domain, host, ip)
                try:
                    data = '{"plugin":"%s", "domain":"%s", "name":"%s", "content":"%s"}' % (plugin, domain, host, ip)
                    response = requests.request("post", "http://localhost:8080/host", data=data, headers={"Content-Type": "application/json"})
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
