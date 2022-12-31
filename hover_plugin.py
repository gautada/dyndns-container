#!/usr/bin/env python3

"""hoverplugin.py: Provides API functionality for Hover.com using their unofficial API.
    This script is based off one by [Dan Krause](https://gist.github.com/dankrause/5585907). This
    script provides a cli interface for testing."""

__author__  = "Adam T. Gautier"
__credits__ = ["Andrew Barilla", "Dan Krause"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Adam Gautier"
__email__ = "adam@gautier.org"
__status__ = "Development"
    
from dyndns_plugin import DynDNSPlugin, DynDNSPluginException, dyndnslog

import os
import argparse
import datetime
import hashlib
import requests
import json
import time

import sys
# import yaml

class HoverPlugin(DynDNSPlugin):
    HOST_RECORD_TYPES = ['A', 'CNAME']
    FIELD_RECORD_TYPE = ['TXT']
    
    def __init__(self, username, password, url="https://www.hover.com/api/"):
        assert url is not None, "URL cannot be null."
        assert username is not None, "Username cannot be null."
        assert password is not None, "Password cannot be null."
        self.__hash = hash = hashlib.md5(password.encode())
        self.__url = url
        self.__cookies = None
        self.__call("post", "login", data={"username": username, "password": password})
        self.__cookies = {"hoverauth": self.__last_response.cookies["hoverauth"]}
        self.__cache = None
        
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
            
    def records(self, domain, force=False):
        assert domain is not None, "Domain cannot be null."
        if self.__cache is None:
            self.__cache = {}
        if domain not in self.__cache:
            self.__cache[domain] = []

        ttl = 60 * 60 * 24 # TTL 1 Week
        last = 0
        delta = 0
        _now = datetime.datetime.now().timestamp()
        for record in self.__cache[domain]:
            
            if DynDNSPlugin.KEY_TTL in record and int(record[DynDNSPlugin.KEY_TTL]) < ttl:
                ttl = int(record[DynDNSPlugin.KEY_TTL])
            if DynDNSPlugin.KEY_LAST in record:
                _last = float(record[DynDNSPlugin.KEY_LAST])
                _delta = _now - _last
                if last < _last:
                    last = _last
                if delta < _delta:
                    delta = _delta
            else:
                record[DynDNSPlugin.KEY_LAST] = _now
        if 0 == delta or ttl <= delta or force:
            records = []
            dyndnslog.warning("Updating records cache for domain(%s)" % domain)
            result = self.__call("get", "domains/%s/dns" % domain)
            assert domain == result["domains"][0]["domain_name"], "Domain must equal %s." % domain
            entries = result["domains"][0]["entries"]
            for entry in entries:
                records.append({
                    DynDNSPlugin.KEY_ID: entry['id'],
                    DynDNSPlugin.KEY_NAME: entry['name'],
                    DynDNSPlugin.KEY_TYPE: entry['type'],
                    DynDNSPlugin.KEY_TTL: entry['ttl'],
                    DynDNSPlugin.KEY_CONTENT: entry['content'],
                    DynDNSPlugin.KEY_LAST: _now
                })
            self.__cache[domain] = records
        
        dyndnslog.info("Records [ttl:%s last:%s delta:%s]" % (ttl, last, delta))
        return self.__cache[domain]

    def record(self, domain=None, record_type=None, name=None, content=None):
        assert domain is not None, "domain cannot be nil."
        assert record_type is not None, "record type cannot be nil."
        assert name is not None, "name cannot be nil."
        
        records = self.records(domain)
        record = None
        for _record in records:
            if name == _record[DynDNSPlugin.KEY_NAME]:
                record = _record
        assert record is not None, "Record(%s) not found in domain(%s)" % (name, domain)
        assert record[DynDNSPlugin.KEY_TYPE] == record_type, "Record type(%s) must match %s" % (record[ynDNSPlugin.KEY_TYPE], record_type)
        
        if content is None:
            return record
        if content == record[DynDNSPlugin.KEY_CONTENT]:
            dyndnslog.info("Skip Update %s.%s already equals %s " % (name, domain, content))
            return record
        
        dyndnslog.info("Updating %s.%s to equal %s " % (name, domain, content))
        record[DynDNSPlugin.KEY_OLD] = record[DynDNSPlugin.KEY_CONTENT]
        self.__call("put", "dns/" + record[DynDNSPlugin.KEY_ID], {"content": content})
        self.records(domain, force=True)
        record[DynDNSPlugin.KEY_CONTENT] = content
        return record
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test cli for HoverPlugin.')
    parser.add_argument('--domain', help='A domain to access')
    parser.add_argument('--record_type', help='The DNS record type (A, TXT, CNAME, ...)accessing')
    parser.add_argument('--name', default=None, help='The DNS record name')
    parser.add_argument('--content', default=None, help='The content value to write into the DNS record')
    parser.add_argument('--username', help='The user name of the hover account')
    parser.add_argument('--password', help='The password of the hover account')
    args = parser.parse_args()

    hover = HoverPlugin(username=args.username, password=args.password)
    records = hover.records(args.domain)
    print("All Records")
    for record in records:
        print(record)
    print("-------------")
    
    
    if args.name is not None:
        print("Record: %s (current value)" % args.name)
        record = hover.record(domain=args.domain, record_type=args.record_type, name=args.name, content=None)
        print( record )
        print()
    
    if args.content is not None:
        print("Record: %s (new value)" % args.name)
        record = hover.record(domain=args.domain, record_type=args.record_type, name=args.name, content=args.content)
        print( record )
        print
