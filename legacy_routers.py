# Team: RGB Alphas
# Date: 10/18/2020
# Project: Programming Assignment 4

#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    r4 = net.addHost('r4', cls=Node, ip='10.0.2.0/24')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    r3 = net.addHost('r3', cls=Node, ip='192.168.1.1/24')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    r5 = net.addHost('r5', cls=Node, ip='192.168.3.1/24')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.0/24', defaultRoute='via 192.168.1.1')
    h2 = net.addHost('h2', cls=Host, ip='10.0.3.0/24', defaultRoute='via 192.168.3.1')

    info( '*** Add links\n')
    net.addLink(s1, h1)
    net.addLink(r3, s1)
    net.addLink(r3, r4, intfName2='r3-eth1',params2={ 'ip' : '192.168.1.0/24'})
    net.addLink(r4, r5, intfName2='r5-eth1',params2={ 'ip' : '192.168.3.0/24'})
    net.addLink(r5, s2)
    net.addLink(s2, h2)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

