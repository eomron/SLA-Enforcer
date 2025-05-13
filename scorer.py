import ipaddress
import socket
import requests
import struct
import subprocess

class ScoreChecker:
    def __init__(self,name: str,ip: str,port: int,*args):
        self.name: str = name
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise ValueError(f"Error on ScoreChecker object {self.name}: Invalid IP address {ip}. Format as a standard IPv4 address. Do not use CIDR postfixes (i.e. /24, /17).")
        self.ip: str = ip
        self.port: int = port
        self.type: str = "ping" if len(args) == 0 else args[0] #when calling the arguments list, remember that args[0] is the type of check
        arguments = args


    def url(self,protocol: str): #several checks call the target as a webpage; this method fetches the data.
        protocol = protocol.lower()
        if protocol != "http" and protocol != "https":
            raise ValueError(f"Error on ScoreChecker object {self.name}: Invalid protocol (should be http or https)")
        response = requests.get(protocol + "://" + self.ip + ":" + str(self.port))
        return [response.status_code,response.text]

    def ping(self):
        try:
            with socket.create_connection((self.ip,self.port),timeout=4):
                return(True)
        except(socket.timeout, ConnectionRefusedError, OSError):
                return(False)

    def httpcontent(self):
        pass

    def index(self):
        pass

    def dns(self):
        pass

    def smb(self):
        pass



    def test(self): #maps self.type to the method to call
        methods = {
            "ping": self.ping,
            "content": self.content,
            "index": self.index,
            "dns": self.dns,
            "smb": self.smb
        }
        if self.type not in methods:
            raise ValueError(f"Unknown test type \"{self.type}\"")
        return methods[self.type](self.arguments)

    

        #with ThreadPoolExecutor(10) as pool: #Not sure where i go from here

        #if self.type == "ping": #check if a port is listening. TODO: implement support for UDP 
        #    pass #link it up later


#        if self.type == "content": #check for a certain string in the HTTP/HTTPS response
#            pass
#        if self.type == "index": #check that <ip>/index.html responds with 200 OK. good for testing if a website is up
#            pass
#        if self.type == "dns": #check that the target (a DNS server) responds with a specific record
#            pass
#        if self.type == "smb": #check that a SMB share on the target is accessible
#            pass

