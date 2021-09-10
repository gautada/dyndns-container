#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import dns.resolver
# import dns.exceptions.Timeout

# HTTPRequestHandler class
class DockerHealthService(BaseHTTPRequestHandler):
    def lookupDNS(self, params={'server':'172.16.0.5','domain':'aegaeon.gautier.local'}):
        print("Lookup: %s" % params)
        ips = []
        msg = 'Not run'
        resp = 0
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers=[params['server']]  # socket.gethostbyname()
            for rdata in resolver.query(params['domain']) :
                ips.append(rdata)
            msg = 'OK'
            resp = 200
        except Exception as ex:
            if 'Timeout' == type(ex).__name__:
                msg = "Server(%s) timeout error" % server
                resp = 408 # 408 Request Timeout
            elif 'NXDOMAIN' == type(ex).__name__:
                msg = "Domain(%s) not found on server(%s)" % (params['domain'], params['server'])
                resp = 404 # 404 Not Found
            else:
                msg = "ERROR(%s/%s): %s" % (type(ex), type(ex).__name__, ex)
                resp = 500 # 500 Internal Server Error
        finally:
            print ("%s = %s [%s %s : %s]" % (params['domain'], ips, params['server'], msg, resp))
            return (params['domain'], ips, params['server'], msg, resp)
    # GET
    def do_GET(self):
        params = {'server':'172.16.0.5','domain':'aegaeon.gautier.local'}
        if '?' in self.requestline:
            print("REQUEST")
            raw = self.requestline.split(' ')[1]
            raw = raw.split('?')[1]
            raw = raw.split('&')
            print(raw)
            print("*******")
            for param in raw:
                param = param.split('=')
                params[param[0]] = param[1]
        print(params)
        dns = self.lookupDNS(params)
        ips = ""
        for ip in dns[1]:
            ips += "%s," % ip
        if 200 == dns[4]:
            str = "%s = %s" % (dns[0], ips[:-1])
        else:
            str = "%s = %s [%s %s : %s]" % (dns[0], ips[:-1], dns[4], dns[2], dns[3])
        self.send_response(dns[4], dns[3])
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(bytearray(str, 'utf-8'))

def run():
    print('starting server...')
    server_address = ('0.0.0.0', 80)
    httpd = HTTPServer(server_address, DockerHealthService)
    print('running server...')
    httpd.serve_forever()

run()
