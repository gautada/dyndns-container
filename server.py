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

class Host(BaseModel):
    plugin: str
    domain: str
    name: str
    content: str

class Field(BaseModel):
    plugin: str
    domain: str
    name: str
    content: str
    
app = FastAPI()
dyndns = DynDNS()

@app.get("/ip")
def read_ip():
    return {
     "status": "success",
     "IP": dyndns.ip
    }

@app.get("/host/{plugin}/{domain}/{name}")
def get_host(plugin: str, domain: str, name: str):
    try:
        rtn = dyndns.host(plugin=plugin, domain=domain, name=name)
        return {"status": "success",
                "host": rtn}
    except Exception as e:
        return {"status": "exception",
                "message": "%s" % e}

@app.post("/host")
def update_host(host: Host):
    try:
        rtn = dyndns.host(plugin=host.plugin, domain=host.domain, name=host.name, content=host.content)
        return {"status": "success",
                "host": rtn}
    except Exception as e:
        return {"status": "exception",
                "message": "%s" % e}

@app.get("/field/{plugin}/{domain}/(name}")
def get_field(plugin: str, domain: str, name: str):
    try:
        rtn = dyndns.field(plugin=plugin, domain=domain, name=name)
        return { "status": "success",
                "field": rtn }
    except Exception as e:
        return { "status": "exception",
                "message": "%s" % e }

@app.post("/field")
def update_host(field: Field):
    try:
        rtn = dyndns.field(plugin=field.plugin, domain=field.domain, name=field.name, content=field.content)
        return { "status": "success",
                "field": rtn }
    except Exception as e:
        return {"status": "exception",
                "message": "%s" % e}


"""
@app.post("/field/{plugin}/{domain}/{field}/")
def update_field(ip: str):
"""
