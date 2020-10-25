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

	ip_r1 = '10.0.1.0/24'
	ip_r2 = '10.0.2.0/24'
	ip_r3 = '10.0.3.0/24'

	net = Mininet( topo=None,
						build=False,
						ipBase=ip_r1)

	info( '*** Adding controller\n' )
	c0=net.addController(name='c0',
							controller=Controller,
							protocol='tcp',
							port=6633)

	info( '*** Add switches\n')
	s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
	s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
	

	info( '*** Add routers\n')

	r1 = net.addHost('r1', cls=None, ip=ip_r1)
	r1.cmd('sysctl -w net.ipv4.ip_forward=1')
	r2 = net.addHost('r2', cls=None, ip=ip_r2)
	r2.cmd('sysctl -w net.ipv4.ip_forward=1')
	r3 = net.addHost('r3', cls=None, ip=ip_r3)
	r3.cmd('sysctl -w net.ipv4.ip_forward=1')

	info( '*** Add hosts\n')
	h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute='via 10.0.1.1')
	h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute='via 10.0.3.1')
	
	info( '*** Add links\n')
	# West
	net.addLink(r1, s4, 
					intfName2='r1-eth0', 
					params2={ 'ip' : ip_r1,})

	net.addLink(s4, h1, intfName1='r1-eth1', params1={ 'ip' : '10.0.1.1/12' })

	# Middle
	net.addLink(r1, r2, 
					intfName1='r2-eth0', 
					intfName2='r2-eth1',
					params1={ 'ip' : '10.100.0.1/24' },
					params2={ 'ip' : '10.100.0.2/24' } )

	# net.addLink(r3, r2, intfName1='r2-eth1', params1={ 'ip' : '10.0.2.1/12' })

	# East
	net.addLink(r3, s5, intfName2='r3-eth0', params2={ 'ip' : ip_r3 })
	net.addLink(s5, h2, intfName1='r3-eth1', params1={ 'ip' : '10.0.3.1/12' })

	net['r1'].cmd('ip route add 10.0.2.0/24 via 10.100.0.2 dev r2-eth1')
	net['r2'].cmd('ip route add 10.0.1.0/24 via 10.100.0.1 dev r2-eth0')

	#net['r2'].cmd('route add -net 10.0.2.0/12 gw 10.0.1.0 eth0')
	#net['r2'].cmd('route add -net 10.0.2.0/12 gw 10.0.3.0 eth0')

	#net['r3'].cmd('route add -net 10.0.3.0/12 gw 10.0.1.0 eth0')
	#net['r3'].cmd('route add -net 10.0.3.0/12 gw 10.0.2.0 eth0')

	info( '*** Starting network\n')
	net.build()
	info( '*** Starting controllers\n')
	for controller in net.controllers:
		controller.start()

	info( '*** Starting switches\n')
	net.get('s5').start([c0])
	net.get('s4').start([c0])

	info( '*** Post configure switches and hosts\n')

	CLI(net)
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	myNetwork()