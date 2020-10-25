#!/usr/bin/python
# Team: RGB Alphas
# Date: 10/18/2020
# Project: Programming Assignment 4

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
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    r3 = net.addHost('r3', cls=Node, ip='10.0.1.1/24')
    r4 = net.addHost('r4', cls=Node, ip='192.168.10.5/24')
    r5 = net.addHost('r5', cls=Node, ip='192.168.20.10/24') 
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.5/24', defaultRoute='via 10.0.1.1')
    h2 = net.addHost('h2', cls=Host, ip='10.0.2.5/24', defaultRoute='via 10.0.2.1')

    info( '*** Add links\n')
    net.addLink(s1, h1, intfName2= 'h1-eth1',params2={ 'ip' : '10.0.1.1/24'})
    net.addLink(s1, r3, intfName2= 'h3-eth1',params2={ 'ip' : '10.0.1.1/24'})
    net.addLink(r4, r3, intfName2= 'r3-eth2',params2={ 'ip' : '192.168.10.10/24'}) 
    net.addLink(r5, r4, intfName2= 'r4-eth1',params2={ 'ip' : '192.168.20.5/24'})
    net.addLink(s2, r5, intfName2= 'r5-eth1',params2={ 'ip' : '10.0.2.1/24'})
    net.addLink(s2, h2, intfName2= 'h2-eth1',params2={ 'ip' : '192.168.20.10/24'})

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')
    r3.cmdPrint( 'ip route add 10.0.2.0/24 via 192.168.10.5 dev r3-eth2' )
    r4.cmdPrint( 'ip route add 10.0.2.0/24 via 192.168.20.10 dev r4-eth1' )    
    r4.cmdPrint( 'ip route add 10.0.1.0/24 via 192.168.10.10 dev r4-eth0' )
    r5.cmdPrint( 'ip route add 10.0.1.0/24 via 192.168.20.5 dev r5-eth0' )

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
