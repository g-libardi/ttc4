#!/usr/bin/env python3
"""
Topology module for BGP network
Contains the NetTopo class for creating Mininet topologies
"""

from mininet.topo import Topo
from mininet.log import info
from .config import TOPOLOGY


class NetTopo(Topo):
    """Topology for BGP network"""
    
    def build(self):
        # Create all nodes from unified config
        self._create_nodes()
        # Create all links from unified config
        self._create_links()
    
    def _create_nodes(self):
        """Create all nodes based on unified configuration"""
        info('*** Criando nós da topologia ***\n')
        
        for as_name, as_config in TOPOLOGY.autonomous_systems.items():
            info(f'*** Criando nós do {as_name} ({as_config.as_type}) ***\n')
            for node in as_config.nodes:
                self.addHost(node.name)
    
    def _create_links(self):
        """Create all links based on unified configuration"""
        info('*** Criando links da topologia ***\n')
        
        # Create intra-AS links
        for as_name, as_config in TOPOLOGY.autonomous_systems.items():
            if as_config.intra_links:
                info(f'*** Criando links intra-AS do {as_name} ***\n')
                for link in as_config.intra_links:
                    self.addLink(link.node1, link.node2, intfName1=link.intf1, intfName2=link.intf2)
        
        # Create inter-AS links
        info('*** Criando links inter-AS ***\n')
        for link in TOPOLOGY.inter_as_links:
            self.addLink(link.node1, link.node2, intfName1=link.intf1, intfName2=link.intf2)
        
        # Create host links
        info('*** Criando links para hosts ***\n')
        for as_name, as_config in TOPOLOGY.autonomous_systems.items():
            if as_config.host_networks:
                router = as_config.get_routers()[0]
                host = as_config.get_hosts()[0]
                host_intf = as_config.host_networks[0].host_intf
                host_eth = f"{host}-eth0"
                self.addLink(router, host, intfName1=host_intf, intfName2=host_eth) 