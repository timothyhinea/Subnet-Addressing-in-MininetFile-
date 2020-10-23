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

    # topology constructor ()
    net = Mininet( topo=None,
                   build=False,
                   ipBase='0.0.0.0')

    # Add controller
    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    # Add switches
    info( '*** Add switches\n')
    s1, s2 = [ net.addSwitch(s) for s in ('s1', 's2') ]

    # Add routers
    r3 = net.addHost('r3', cls=Node, ip='0.0.0.0')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    r4 = net.addHost('r4', cls=Node, ip='0.0.0.0')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    r5 = net.addHost('r5', cls=Node, ip='0.0.0.0')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Add hosts
    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.0/24', defaultRoute='via 10.0.1.0')
    h2 = net.addHost('h2', cls=Host, ip='10.0.2.0/24', defaultRoute='via 10.0.2.0')

    info( '*** Add links\n')
    net.addLink(h1, s1, intfName2='s1-eth1', params2={ 'ip' : ' 10.0.1.0/24'})
    net.addLink(s1, r3, intfName2='r3-eth0', params2={ 'ip' : ' 10.0.1.0/24'})
    net.addLink(r3, r4, intfName2='r4-eth2', params2={ 'ip' : '192.168.1.0/24'})
    net.addLink(r4, r5, intfName2='r5-eth3', params2={ 'ip' : '192.168.2.0/24'})
    net.addLink(s2, r5, intfName2='r5-eth0', params2={ 'ip' : ' 10.0.2.0/24'})
    net.addLink(h2, s2, intfName2='s2-eth2', params2={ 'ip' : ' 10.0.2.0/24'})

    # Start network
    info( '*** Starting network\n')
    net.build()

    # Start controllers
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    # Start switches
    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()