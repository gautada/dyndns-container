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

# from dyndns_plugin import DynDNSPluginException, dyndnslog

class DynDNSClient():
    
    def __init__(self, url, verbose=False):
        self.__url = url
        self.__verbose = verbose
        self.__response = None
        
    def __call(self, method, url, data=None):
        response = None
        print("DynDNS __call(%s): %s" % (method, url))
        try:
            self.__response = requests.request(method, url, data=data)
        except Exception as e:
            msg = e
            if hasattr(e, 'message'):
                msg = e.message
            raise Exception("Exception(%s): %s" % (type(e), msg))
        if self.__response.ok:
            body = self.__response.json()
            if "status" not in body or body["status"] != 'success':
                raise Exception("%s: (%s) %s" % (self.__response.url, self.__response.status_code, self.__response.text))
            return body
        else:
            raise Exception("%s: (%s) %s" % (self.__response.url, self.__response.status_code, self.__response.text))
        return response.json()
    
    @property
    def url(self):
        return self.__url
        
    @property
    def verbose(self):
        return self.__verbose
    
    @property
    def response(self):
        return self.__response
    
    @property
    def ip(self):
        response = self.__call("get", "%s/ip" % self.url)
        print(response)
        return response['IP']['current']
        
    def record(self, plugin=None, domain=None, record_type=None, name=None, content=None):
        assert plugin is not None, "plugin cannot be nil."
        assert domain is not None, "domain cannot be nil."
        assert record_type is not None, "record type cannot be nil."
        assert name is not None, "name cannot be nil."
        if content is None:
            return self.__call("get", "%s/record/%s/%s/%s/%s" % (self.url, plugin, domain, record_type, name))
        else:
            data = '{"value":"%s"}' % (content)
            print("Pushing data %s" % data)
            return self.__call("post", "%s/record/%s/%s/%s/%s" % (self.url, plugin, domain, record_type, name), data=data)
        
        
def main(args):
    client = DynDNSClient(url=args.url, verbose=args.verbose)
    if "ip" == args.command:
        print(client.ip)
    elif "record" == args.command:
        print(client.record(plugin=args.plugin, domain=args.domain, record_type=args.record_type, name=args.name, content=args.content))
        
def record_command():
    print("record command")
    
if __name__ == "__main__":
    parent_parser = argparse.ArgumentParser(description='Test cli for DynDNS Client.', add_help=False)
    parent_parser.add_argument('--url', default='http://localhost:8080', help='API endpoint url')
    parent_parser.add_argument('--verbose', action=argparse.BooleanOptionalAction, help='Verbose output')
    
    main_parser = argparse.ArgumentParser()
    subparsers = main_parser.add_subparsers(title="command", dest="command")
                    
    parser_ip = subparsers.add_parser('ip', help='Returns the current IP address', parents=[parent_parser])
    
    record_parser = subparsers.add_parser('record', help='Manages DNS records', parents=[parent_parser])
    record_parser.add_argument('--plugin', default='hover', help='The plugin to use for the calls')
    record_parser.add_argument('--domain', help='A domain to access')
    record_parser.add_argument('--record_type', help='The DNS record type (A, TXT, CNAME, ...)accessing')
    record_parser.add_argument('--name', default=None, help='The DNS record name')
    record_parser.add_argument('--content', default=None, help='The content value to write into the DNS record')

    args = main_parser.parse_args()
    
    main(args)
