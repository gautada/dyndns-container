#!/usr/bin/env python3

"""dyndns_plugin.py: Plugin to interface with DNS provided for dynamic dns service"""

__author__  = "Adam T. Gautier"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Adam Gautier"
__email__ = "adam@gautier.org"
__status__ = "Development"

import logging

logging.basicConfig(level=logging.INFO)
dyndnslog = logging.getLogger("dyndns")

class DynDNSException(Exception):
    pass
    
class DynDNSPluginException(DynDNSException):
    pass
    
class DynDNSPlugin(object):
    KEY_ID = "id"
    KEY_NAME = "name"
    KEY_TYPE = "type"
    KEY_TTL = "ttl"
    KEY_CONTENT = "content"
    KEY_LAST = "last"
    KEY_OLD = "old"
    
    def record(self, domain, record_type, name, content=None):
        raise DynDNSPluginException("Method not implemented")
        
    def records(self, domain):
        raise DynDNSPluginException("Method not implemented")
    
