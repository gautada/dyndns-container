#!/usr/bin/env python3

"""dyndns_service.py: A rolled up interface to the dynamic dns service, this handles all plugins and configuration handling"""

__author__  = "Adam T. Gautier"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Adam Gautier"
__email__ = "adam@gautier.org"
__status__ = "Development"

from fastapi import FastAPI
from pydantic import BaseModel
from dyndns import DynDNS

class Content(BaseModel):
    value: str
    
app = FastAPI()
dyndns = DynDNS()

@app.get("/ip")
def get_ip():
    return { "status": "success", "IP": dyndns.ip }

@app.get("/record/{plugin}/{domain}/{record_type}/{name}")
def get_record(plugin: str, domain: str, record_type: str, name: str):
    try:
        rtn = dyndns.record(plugin=plugin, domain=domain, record_type=record_type, name=name)
        return {"status": "success", "host": rtn}
    except Exception as e:
        return {"status": "exception", "message": "%s" % e}

@app.post("/record/{plugin}/{domain}/{record_type}/{name}")
def post_record(plugin: str, domain: str, record_type: str, name: str, content: Content):
    try:
        rtn = dyndns.record(plugin=plugin, domain=domain, record_type=record_type, name=name, content=content.value)
        return {"status": "success", "host": rtn}
    except Exception as e:
        return {"status": "exception", "message": "%s" % e}

"""
@app.get("/health")
def read_ip():
    return {
     "status": "success",
     "health": True
    }
"""
