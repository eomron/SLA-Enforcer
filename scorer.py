import ipaddress
import socket
import requests
import struct
import subprocess
import sys
import os

if __name__ == "__main__" and os.path.basename(sys.argv[0]) != "run.py": #if we run this file by accident, it executes run.py anyway
    import run
    run.main()
    sys.exit()

class ScoreChecker:
    def __init__(self,name: str,ip: str,port: int,type: str,*args):
        """
        Initializes the information about the check; validates the IP address.

        Args:
            str: The name of this check.
            str: The IP address of the target.
            int: The port of the service to check on the target.
            str: The type of check. Valid types are listed in the documentation.
            tuple: Any further arguments, depending on the type of check.
        """
        self.name: str = name
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise ValueError(f"Error on ScoreChecker object {self.name}: Invalid IP address {ip}. Format as a standard IPv4 address. Do not use CIDR postfixes (i.e. /24, /17).")
        self.ip: str = ip
        self.port: int = port
        self.type: str = type
        self.arguments = args


    def url(self,*args) -> tuple:
        """
        Calls the target as a webpage.

        Args:
            str: The path to the desired page, relative to the IP address. For example, "auth/login/success".
            str: Either "https" or "http". Must be specified if a non-default port (not 80 or 443) is being used.
            tuple: This method takes any number of arguments, but further arguments are ignored.

        Returns:
            tuple: A tuple containing an int (the HTTP status code of the page) and a str (the data from the response).

        """
        protocol: str = ""
        if args[1] == "https" or self.port == 443:
            protocol = "https"
        elif args[1] == "http" or self.port == 80:
            protocol = "http"
        else:
            raise ValueError(f"Error on ScoreChecker object {self.name}: Invalid protocol (should be http or https)")
        protocol = protocol.lower()
        page: str = args[0] if len(args) > 0 else ""
        page = page.strip("/")
        response = requests.get(protocol + "://" + self.ip + ":" + str(self.port) + "/" + page,verify=False) #this ignores SSL by design because most training scenarios are going to be self-signed.
        return (response.status_code,response.text)

    def ping(self,*args) -> bool: #TODO: implement support for UDP 
        '''
        Attempts to connect to the target on the specified port.

        Args:
            tuple: This method takes any number of arguments, but all are ignored.

        Returns:
            bool: Whether or not the attempt to connect was successful.
        '''
        try:
            with socket.create_connection((self.ip,self.port),timeout=4):
                return(True)
        except(socket.timeout, ConnectionRefusedError, OSError):
                return(False)

    def content(self,*args) -> bool:
        '''
        Checks that the target webpage contains a specific string.

        Args:
            str: The path to the desired page, relative to the IP address. For example, "auth/login/success".
            str: Either "https" or "http". Must be specified if a non-default port (not 80 or 443) is being used.
            str: The desired string to be found in the webpage.
            tuple: This method takes any number of arguments, but further arguments are ignored.

        Returns:
            bool: Whether or not the content was found.
        '''
        if len(args) > 2:
            return(args[2] in self.url(args)[1])
        else:
            raise TypeError(f"Error on ScoreChecker object {self.name}: Type is declared as \"content\", but not enough arguments are supplied (requires at least 3).")

    def pageExists(self,*args) -> bool:
        #for this function, the line should be:
        #name,ip,port,pageExists,<webpage>,<protocol> (remove this comment when i write documentation for config.csv)
        """
        Checks whether a webpage responds with a specific status code, default is 200.
        
        Args:
            str: The path to the desired page, relative to the IP address. For example, "auth/login/success". Set as an empty string if you wish to access the raw IP address.
            str: Either "https" or "http". Must be specified if a non-default port (not 80 or 443) is being used.
            int: The desired status code.
            tuple: This method takes any number of arguments, but further arguments are ignored.

        Returns:
            bool: Whether the specific status code was received.
        """
        statusCode = args[2] if len(args) > 2 else 200
        return self.url(args)[0] == statusCode

    def dns(self,*args) -> bool:
        """
        
        
        """
        pass

    def smb(self):
        pass


    def test(self): #maps self.type to the method to call
        methods = {
            "ping": self.ping,
            "content": self.content,
            "pageExists": self.pageExists,
            "dns": self.dns,
            "smb": self.smb
        }
        if self.type not in methods:
            raise ValueError(f"Unknown test type \"{self.type}\"")
        return methods[self.type](self.arguments) #because of how this is written, every method listed here must take a tuple in its arguments