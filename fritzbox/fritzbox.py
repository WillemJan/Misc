#!/usr/bin/env python

"""
    FRITZ!Box_arpwatch program will display the mac addrs known on the FRITZ!Box.
    Enable telnet on modem : #96*7* 

    Copyright (C) 2010 Faber, Willem Jan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pexpect, time, sys, re, os

TIMEOUT = 3

class FritzBox(object):
    config = {}
    arp_cache = [] 

    def __init__(self, password = None, remote_ip = "10.0.0.138", echo = {}):
        self.config = {"PASSWORD" : password, "REMOTE_IP" : remote_ip}
        self.echo = echo

        if os.path.isfile("/tmp/arp"):
            tmp_file = open("/tmp/arp", "r")
            data = tmp_file.read()
            i = 0

            for line in data.split('\n'):
                if len(line.strip()) > 0:
                    self.arp_cache.append(line.strip())
                    i += 1

            if "status" in self.echo.keys():
                if self.echo["status"]:
                    print("%i macs from cache.." % i)

            tmp_file.close()

    def run_arpwatch(self):
        if self._run_command('cat /proc/net/arp'):
            i = j = 0

            for line in self.child:
                mac_addr = False
                ip = False

                for data in line.strip().split(" "):
                    if re.compile("([A-F0-9]{2}:?){6}").search(data):
                        mac_addr = data
                    if re.compile("([0-9]{1,2}\.?){4}").search(data):
                        ip = data

                if mac_addr not in self.arp_cache and ip:
                    self.arp_cache.append(mac_addr)
                    tmp_file = open("/tmp/arp", "a")
                    tmp_file.write(mac_addr + "\n")
                    tmp_file.close()
                    if "new" in self.echo.keys():
                        if self.echo["new"]:
                            sys.stdout.write("new mac_addr:\t%s \t ip:%s\n" % (mac_addr, ip))
                elif ip:
                    if "known" in self.echo.keys():
                        if self.echo["known"]:
                            sys.stdout.write("known mac_addr:\t%s \t ip:%s\n" % (mac_addr, ip))

            self.child.close()

            if "status" in self.echo.keys():
                if self.echo["status"]:
                    sys.stdout.write("FRITZ!Box up \n")

            return(True)

        else:
            if "error" in self.echo.keys():
                if self.echo.keys["error"]:
                    sys.stdout.write("telnet " + self.config["REMOTE_IP"] + " failed!\n")

            if "status" in self.echo.keys():
                if self.echo.keys["status"]:
                    sys.stdout.write("FRITZ!Box down \n")

            return(False)

    def _run_command(self, cmd):
        self.child = pexpect.spawn ('telnet ' + self.config["REMOTE_IP"])

        try:
            self.child.expect('Fritz!Box web password: ', timeout=TIMEOUT)
            self.child.sendline (self.config["PASSWORD"]+'\r\r')
            conn=self.child.expect ('# ', timeout = TIMEOUT)
        except:
            self.child.terminate()
            self.child.close()
            return(False)

        self.child.sendline (cmd + '\n\rexit\n\r')
        self.child.terminate()
        return(True)

if __name__ == "__main__":
    fb=FritzBox(password = "password_here", echo={"new" : True, "status" : False, "known" : False})
    fb.run_arpwatch()
    sys.stdout.flush()
