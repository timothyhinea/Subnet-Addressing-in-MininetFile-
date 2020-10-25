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
	ipBase='192.168.1.1/8')

	info( '*** Adding controller\n' )
	c0=net.addController(name='c0',
	controller=Controller,
	protocol='tcp',
	port=6633)

	info( '*** Add switches\n')
	s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
	s2 = net.addSwitch('s2', cls=OVSKernelSwitch)

	r1 = net.addHost('r1', cls=Node)
	r1.cmd('sysctl -w net.ipv4.ip_forward=1')

	r2 = net.addHost('r2', cls=Node)
	r2.cmd('sysctl -w net.ipv4.ip_forward=1')

	r3 = net.addHost('r3', cls=Node)
	r3.cmd('sysctl -w net.ipv4.ip_forward=1')

	info( '*** Add hosts\n')
	h1 = net.addHost('h1', cls=Host, defaultRoute='via 192.168.1.1')
	h2 = net.addHost('h2', cls=Host, defaultRoute='via 172.168.1.1')

#	h1.cmdPrint( 'slogin 192.168.1.1' )
#	r1.cmdPrint( 'slogin 216.168.1.5' )
#	r2.cmdPrint( 'slogin 172.168.1.2' )
#	r3.cmdPrint( 'slogin 216.168.1.6' )

	net.addLink(h1, s1,
			intfName1='h1-eth0',
			params1={ 'ip' : '10.1.0.1/24' },
			intfName2='s1-eth0',
			params2={ 'ip' : '10.1.1.1/24' })

	net.addLink(s1, r1,
			intfName1='s1-eth1',
			params1={ 'ip' : '10.1.1.2/24' },
			intfName2='r1-eth0',
			params2={ 'ip' : '192.168.1.1/8' })

	net.addLink(r1, r2,
			intfName1='r1-eth1',
			params1={ 'ip' : '192.168.1.2/8' },
			intfName2='r2-eth0',
			params2={ 'ip' : '216.168.1.5/8' })

	net.addLink(r2, r3,
			intfName1='r2-eth1',
			params1={ 'ip' : '216.168.1.6/8' },
			intfName2='r3-eth1',
			params2={ 'ip' : '172.168.1.2/8' })

	net.addLink(r3, s2,
			intfName1='r3-eth0',
			params1={ 'ip' : '172.168.1.1/8' },
			intfName2='s2-eth1',
			params2={ 'ip' : '10.2.1.2/24' })

	net.addLink(s2, h2,
			intfName1='s2-eth0',
			params1={ 'ip' : '10.2.1.1/24' },
			intfName2='h2-eth0',
			params2={ 'ip' : '10.2.0.1/24' })

	info( '*** Starting network\n')
	net.build()

	info( '*** Starting controllers\n')
	for controller in net.controllers:
		controller.start()

	info( '*** Starting switches\n')
	net.get('s2').start([c0])
	net.get('s1').start([c0])

	info( '*** Post configure switches and hosts\n')
	r1.cmdPrint( 'ip route add 172.168.1.2 via 192.168.1.2 dev r1-eth1' )
	r2.cmdPrint( 'ip route add 172.168.1.2 via 216.168.1.6 dev r2-eth1' )
	r2.cmdPrint( 'ip route add 192.168.1.2 via 216.168.1.6 dev r2-eth1' )
	r3.cmdPrint( 'ip route add 192.168.1.2 via 172.168.1.2 dev r3-eth1' )

#	r1.cmdPrint( 'ip route add 10.0.2.0 via 192.168.1.1 dev r1-eth1' )
#	r2.cmdPrint( 'ip route add 10.0.1.0 via 192.168.1.2 dev r2-eth0' )
#	r2.cmdPrint( 'ip route add 10.0.2.0 via 192.168.2.2 dev r2-eth1' )
#	r3.cmdPrint( 'ip route add 10.0.1.0 via 192.168.2.1 dev r3-eth0' )

	CLI(net)
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	myNetwork()
