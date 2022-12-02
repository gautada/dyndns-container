#!/usr/bin/env python3

"""hover.py: Provides dynamic DNS functionality for Hover.com using their unofficial API.
    This script is based off one by Dan Krause: https://gist.github.com/dankrause/5585907"""

__author__  = "Adam T. Gautier"
__credits__ = ["Andrew Barilla", "Dan Krause"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Adam Gautier"
__email__ = "adam@gautier.org"
__status__ = "Development"

import os
import argparse
import hashlib
import requests
import json
import time
import logging
import sys
import yaml

# Sign into hover.com and then go to: https://www.hover.com/api/domains/YOURDOMAIN.COM/dns
# Look for the subdomain record that you want to update and put its id here.

SLEEPTIME = 60

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dydns")

class HoverException(Exception):
    pass

class HoverAPI(object):
    def __init__(self, username, password):
        params = {"username": username, "password": password}
        r = requests.post("https://www.hover.com/api/login", data=params)
        if not r.ok or "hoverauth" not in r.cookies:
            print(r.text)
            raise HoverException(r)
        self.cookies = {"hoverauth": r.cookies["hoverauth"]}
    
    def call(self, method, resource, data=None):
        url = "https://www.hover.com/api/{0}".format(resource)
        logger.info("%s" % url)
        r = requests.request(method, url, data=data, cookies=self.cookies)
        if not r.ok:
            print(r)
            raise HoverException(r)
        if r.content:
            body = r.json()
            if "succeeded" not in body or body["succeeded"] is not True:
                raise HoverException(body)
            return body

def daemon(domains=None, host=None, user=None, password=None, sleep=60):
    while True:
        try:
            for fqdn in domains: # domains.split(','):
                fqdn = fqdn.strip()
                split = fqdn.split('.')
                assert 3 == len(split), "Domain[%s] must be fully qualified as 'host.domain.tld'" % fqdn
                host = split[0]
                domain = "%s.%s" % (split[1], split[2])

                ip = None
                old_ip = None
                new_ip = None
                
                print()
                print("Starting dynamic dns daemon for %s" % fqdn)
                
                try:
                    ip = requests.get("https://api.ipify.org")
                    new_ip = ip.text
                except:
                    msg ="Unable to get IP address from ipify service"
                    print("Error: %s" % msg)
            
                if ip.ok and (old_ip is None or old_ip != new_ip):
                    logger.info("Updating DNS(%s) settings [%s is now %s]" % (fqdn, old_ip, new_ip))
                    # connect to the API using your account
                    client = HoverAPI(user, password)
                    result = client.call("get", "domains/%s/dns" % domain)
                    dns_id = None
                    for hhost in result["domains"][0]["entries"]:
                        if hhost['name'] == host:
                            dns_id = hhost['id']
                            print("Using id[%s] for %s" % (dns_id, fqdn))
                    if dns_id is None:
                        raise HoverException("Unable to determine DNS ID for %s" % fqdn)
                    print("Updating IP for %s to %s" % (fqdn, new_ip))
                    client.call("put", "dns/" + dns_id, {"content": new_ip})
                    old_ip = new_ip
                else:
                    print("No updates sent to Hover [%s]" % old_ip)
                time.sleep(10)
            print("Sleeping %s seconds until next check" % (SLEEPTIME*sleep))
            time.sleep(SLEEPTIME*sleep)
            print("Waking from rest and checking current IP address")
        except KeyboardInterrupt:
                print("Damon ending")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set Dynamic DNS (for Hover) Daemon.')
    parser.add_argument('--config', default=None, help='Path to configuration file')
    parser.add_argument('--domains', default=None, help='Comma delimited list of fully qualified domain names')
    parser.add_argument('--user', help='The user name of the hover account')
    parser.add_argument('--password', help='The password of the hover account')
    parser.add_argument('--sleep', type=int, default=60, help='Minutes to sleep between updates')
    args = parser.parse_args()

    config = None
    if args.config is not None:
        with open(args.config, "r") as file:
            data = file.read()
            config = yaml.safe_load(data)

    user = None
    if 'user' in config.keys():
        user = config['user']
    if 'DYNIP_USER' in os.environ.keys():
        user = os.environ['DYNIP_USER']
    if args.user is not None:
        user = args.user

    password = None
    if 'password' in config.keys():
        password = config['password']
    if 'DYNIP_PASSWORD' in os.environ.keys():
        password = os.environ['DYNIP_PASSWORD']
    if args.password is not None:
        password = args.password
   
    sleep = args.sleep
    if 'sleep' in config.keys():
        sleep = config['sleep']
    if 'DYNIP_SLEEP' in os.environ.keys():
        sleep = os.environ['DYNIP_SLEEP']

    domains = []
    if 'domains' in config.keys():
        for tmp in config['domains']:
            domain = list(tmp.keys())[0]
            hosts = list(tmp.values())[0]
            for host in hosts:
                domains.append("%s.%s" % (host, domain))
    if 'DOMAINS' in os.environ.keys():
        tmp = os.environ['DOMAINS']
        domains = tmp.split(",")
    if args.domains is not None:
        tmp = args.domains
        domains = tmp.split(",")

    hash = hashlib.md5(password.encode())
    print(user, hash.hexdigest(), sleep)
    print(domains)

    daemon(domains=domains, user=user, password=password, sleep=sleep)

