#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.clean import cleanup


class NetTopo(Topo):
        def build(self, **_opts):
                # Core AS1 routers
                ra1 = self.addHost('ra1')
                ra2 = self.addHost('ra2')  
                ra3 = self.addHost('ra3')
                
                # Core AS2 routers
                rb1 = self.addHost('rb1')
                rb2 = self.addHost('rb2')
                rb3 = self.addHost('rb3')
                
                # Core AS3 routers
                rc1 = self.addHost('rc1')
                rc2 = self.addHost('rc2')
                rc3 = self.addHost('rc3')
                
                # Access AS routers and hosts
                rx = self.addHost('rx')    # AS100
                ry = self.addHost('ry')    # AS150 
                rw = self.addHost('rw')    # AS200
                
                # End hosts
                x = self.addHost('x')      # AS100 host
                y = self.addHost('y')      # AS150 host
                w = self.addHost('w')      # AS200 host
                
                # AS1 Intra-AS Links
                self.addLink(ra1, ra3, intfName1='ra1-eth2', intfName2='ra3-eth0')  # 192.168.1.0/30
                self.addLink(ra2, ra3, intfName1='ra2-eth1', intfName2='ra3-eth1')  # 192.168.1.4/30
                self.addLink(ra1, ra2, intfName1='ra1-eth3', intfName2='ra2-eth0')  # 192.168.1.8/30

                # AS2 Intra-AS Links  
                self.addLink(rb1, rb3, intfName1='rb1-eth2', intfName2='rb3-eth0')  # 192.168.2.0/30
                self.addLink(rb2, rb3, intfName1='rb2-eth1', intfName2='rb3-eth1')  # 192.168.2.4/30
                self.addLink(rb1, rb2, intfName1='rb1-eth3', intfName2='rb2-eth0')  # 192.168.2.8/30

                # AS3 Intra-AS Links
                self.addLink(rc1, rc3, intfName1='rc1-eth4', intfName2='rc3-eth0')  # 192.168.3.0/30
                self.addLink(rc2, rc3, intfName1='rc2-eth1', intfName2='rc3-eth1')  # 192.168.3.4/30
                self.addLink(rc1, rc2, intfName1='rc1-eth3', intfName2='rc2-eth0')  # 192.168.3.8/30

                # Core-to-Core Inter-AS Links (BGP Peerings)
                self.addLink(ra1, rc1, intfName1='ra1-eth0', intfName2='rc1-eth0')  # 10.0.0.0/30
                self.addLink(ra1, rb1, intfName1='ra1-eth1', intfName2='rb1-eth0')  # 10.0.0.4/30

                # Core-to-Access Inter-AS Links  
                self.addLink(rb1, rx, intfName1='rb1-eth1', intfName2='rx-eth0')    # 10.0.0.8/30
                self.addLink(rc1, rx, intfName1='rc1-eth1', intfName2='rx-eth1')    # 10.0.0.12/30
                self.addLink(rc1, ry, intfName1='rc1-eth2', intfName2='ry-eth0')    # 10.0.0.16/30
                self.addLink(ra1, rw, intfName1='ra1-eth4', intfName2='rw-eth0')    # 10.0.0.24/30

                # Access router to host links
                self.addLink(rx, x, intfName1='rx-eth2', intfName2='x-eth0')        # 192.168.100.0/24
                self.addLink(ry, y, intfName1='ry-eth1', intfName2='y-eth0')        # 192.168.150.0/24  
                self.addLink(rw, w, intfName1='rw-eth1', intfName2='w-eth0')        # 192.168.200.0/24


def create_ip_net(net):
        print("create_ip_net")
        # AS1 Intra-AS addressing
        net['ra1'].cmdPrint("ifconfig ra1-eth2 192.168.1.1/30")   # ra1 <-> ra3
        net['ra3'].cmdPrint("ifconfig ra3-eth0 192.168.1.2/30")
        net['ra2'].cmdPrint("ifconfig ra2-eth1 192.168.1.6/30")   # ra2 <-> ra3  
        net['ra3'].cmdPrint("ifconfig ra3-eth1 192.168.1.5/30")
        net['ra1'].cmdPrint("ifconfig ra1-eth3 192.168.1.9/30")   # ra1 <-> ra2
        net['ra2'].cmdPrint("ifconfig ra2-eth0 192.168.1.10/30")

        # AS2 Intra-AS addressing
        net['rb1'].cmdPrint("ifconfig rb1-eth2 192.168.2.1/30")   # rb1 <-> rb3
        net['rb3'].cmdPrint("ifconfig rb3-eth0 192.168.2.2/30")
        net['rb2'].cmdPrint("ifconfig rb2-eth1 192.168.2.6/30")   # rb2 <-> rb3
        net['rb3'].cmdPrint("ifconfig rb3-eth1 192.168.2.5/30")
        net['rb1'].cmdPrint("ifconfig rb1-eth3 192.168.2.9/30")   # rb1 <-> rb2
        net['rb2'].cmdPrint("ifconfig rb2-eth0 192.168.2.10/30")

        # AS3 Intra-AS addressing  
        net['rc1'].cmdPrint("ifconfig rc1-eth4 192.168.3.1/30")   # rc1 <-> rc3
        net['rc3'].cmdPrint("ifconfig rc3-eth0 192.168.3.2/30")
        net['rc2'].cmdPrint("ifconfig rc2-eth1 192.168.3.6/30")   # rc2 <-> rc3
        net['rc3'].cmdPrint("ifconfig rc3-eth1 192.168.3.5/30")
        net['rc1'].cmdPrint("ifconfig rc1-eth3 192.168.3.9/30")   # rc1 <-> rc2
        net['rc2'].cmdPrint("ifconfig rc2-eth0 192.168.3.10/30")

        # Inter-AS BGP peering networks
        net['ra1'].cmdPrint("ifconfig ra1-eth0 10.0.0.1/30")      # ra1 <-> rc1
        net['rc1'].cmdPrint("ifconfig rc1-eth0 10.0.0.2/30")
        net['ra1'].cmdPrint("ifconfig ra1-eth1 10.0.0.5/30")      # ra1 <-> rb1  
        net['rb1'].cmdPrint("ifconfig rb1-eth0 10.0.0.6/30")
        net['rb1'].cmdPrint("ifconfig rb1-eth1 10.0.0.9/30")      # rb1 <-> rx
        net['rx'].cmdPrint("ifconfig rx-eth0 10.0.0.10/30")
        net['rc1'].cmdPrint("ifconfig rc1-eth1 10.0.0.14/30")     # rc1 <-> rx
        net['rx'].cmdPrint("ifconfig rx-eth1 10.0.0.13/30")
        net['rc1'].cmdPrint("ifconfig rc1-eth2 10.0.0.17/30")     # rc1 <-> ry
        net['ry'].cmdPrint("ifconfig ry-eth0 10.0.0.18/30")
        net['ra1'].cmdPrint("ifconfig ra1-eth4 10.0.0.25/30")     # ra1 <-> rw
        net['rw'].cmdPrint("ifconfig rw-eth0 10.0.0.26/30")

        # Access networks and hosts
        net['rx'].cmdPrint("ifconfig rx-eth2 192.168.100.1/24")
        net['x'].cmdPrint("ifconfig x-eth0 192.168.100.2/24")
        net['ry'].cmdPrint("ifconfig ry-eth1 192.168.150.1/24")
        net['y'].cmdPrint("ifconfig y-eth0 192.168.150.2/24")
        net['rw'].cmdPrint("ifconfig rw-eth1 192.168.200.1/24")
        net['w'].cmdPrint("ifconfig w-eth0 192.168.200.2/24")

def config_route(net):
        print("config_route")
        # Enable IP forwarding on all routers
        routers = ['ra1', 'ra2', 'ra3', 'rb1', 'rb2', 'rb3', 'rc1', 'rc2', 'rc3', 'rx', 'ry', 'rw']
        for router in routers:
                net[router].cmdPrint('sysctl -w net.ipv4.ip_forward=1')
        
        # Host default routes
        net['x'].cmdPrint('route add default gw 192.168.100.1')
        net['y'].cmdPrint('route add default gw 192.168.150.1')
        net['w'].cmdPrint('route add default gw 192.168.200.1')
        
        # AS1 internal routing
        net['ra1'].cmdPrint('route add -net 192.168.1.4/30 gw 192.168.1.2 dev ra1-eth2')
        net['ra2'].cmdPrint('route add -net 192.168.1.0/30 gw 192.168.1.5 dev ra2-eth1')
        net['ra3'].cmdPrint('route add -net 192.168.1.8/30 gw 192.168.1.1 dev ra3-eth0')
        
        # AS2 internal routing  
        net['rb1'].cmdPrint('route add -net 192.168.2.4/30 gw 192.168.2.2 dev rb1-eth2')
        net['rb2'].cmdPrint('route add -net 192.168.2.0/30 gw 192.168.2.5 dev rb2-eth1')
        net['rb3'].cmdPrint('route add -net 192.168.2.8/30 gw 192.168.2.1 dev rb3-eth0')

        # AS3 internal routing
        net['rc1'].cmdPrint('route add -net 192.168.3.4/30 gw 192.168.3.2 dev rc1-eth4')
        net['rc2'].cmdPrint('route add -net 192.168.3.0/30 gw 192.168.3.5 dev rc2-eth1')
        net['rc3'].cmdPrint('route add -net 192.168.3.8/30 gw 192.168.3.1 dev rc3-eth0')

def net_test(net):
        print("Network connectivity")
        net['x'].cmdPrint('ping -c 3 192.168.150.2')
        net['x'].cmdPrint('traceroute 192.168.150.2')
        net['y'].cmdPrint('iperf3 -s &')
        net['x'].cmdPrint('sleep 3')
        net['x'].cmdPrint('iperf3 -c 192.168.150.2 -R -t 10 -P 1')

def run():
        topo = NetTopo()
        net = Mininet(topo=topo) #, link=TCLink, switch=OVSBridge, controller=None, host=CPULimitedHost)
        net.start()
        print("Host connections")
        dumpNodeConnections(net.hosts)

        create_ip_net(net)
        config_route(net)

        net_test(net)

        CLI(net)
        net.stop()
        cleanup()

if __name__ == '__main__':
        setLogLevel( 'info' )
        run()