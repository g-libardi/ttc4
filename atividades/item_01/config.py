#!/usr/bin/env python3
"""
Configuration module for BGP topology
Contains all dataclass definitions and centralized topology configuration
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class LinkConfig:
    """Configuration for a network link between two nodes"""
    node1: str
    node2: str
    intf1: str
    intf2: str
    network: str
    ip1: str
    ip2: str
    
    @property
    def mask(self) -> str:
        """Extract network mask from network notation"""
        return self.network.split('/')[1]


@dataclass
class NodeConfig:
    """Configuration for a network node (router or host)"""
    name: str
    node_type: str  # 'router' or 'host'
    default_route: Optional[str] = None  # For hosts


@dataclass
class NetworkConfig:
    """Configuration for a host network"""
    network: str
    host_ip: str
    gateway_ip: str
    host_intf: str  # Interface on router connecting to host
    
    @property
    def mask(self) -> str:
        """Extract network mask from network notation"""
        return self.network.split('/')[1]
    
    @property
    def host_eth(self) -> str:
        """Generate host ethernet interface name"""
        host_name = None
        # Find host name from the network (will be set by AS config)
        for node in self._nodes if hasattr(self, '_nodes') else []:
            if node.node_type == 'host':
                host_name = node.name
                break
        return f"{host_name}-eth0" if host_name else "host-eth0"


@dataclass
class ASConfig:
    """Unified configuration for any AS (core or access)"""
    as_number: str
    as_type: str  # 'core' or 'access'
    nodes: List[NodeConfig]
    intra_links: List[LinkConfig] = field(default_factory=list)
    host_networks: List[NetworkConfig] = field(default_factory=list)
    
    def get_routers(self) -> List[str]:
        """Get all router nodes in this AS"""
        return [node.name for node in self.nodes if node.node_type == 'router']
    
    def get_hosts(self) -> List[str]:
        """Get all host nodes in this AS"""
        return [node.name for node in self.nodes if node.node_type == 'host']
    
    def get_all_nodes(self) -> List[str]:
        """Get all node names in this AS"""
        return [node.name for node in self.nodes]


@dataclass
class TopologyConfig:
    """Complete topology configuration"""
    autonomous_systems: Dict[str, ASConfig]
    inter_as_links: List[LinkConfig]
    
    def get_all_router_nodes(self) -> List[str]:
        """Get all router node names from all ASes"""
        router_nodes = []
        for as_config in self.autonomous_systems.values():
            router_nodes.extend(as_config.get_routers())
        return router_nodes
    
    def get_core_ases(self) -> Dict[str, ASConfig]:
        """Get only core ASes"""
        return {name: config for name, config in self.autonomous_systems.items() 
                if config.as_type == 'core'}
    
    def get_access_ases(self) -> Dict[str, ASConfig]:
        """Get only access ASes"""
        return {name: config for name, config in self.autonomous_systems.items() 
                if config.as_type == 'access'}


# Unified topology configuration using dataclasses
TOPOLOGY = TopologyConfig(
    autonomous_systems={
        'AS1': ASConfig(
            as_number='AS1',
            as_type='core',
            nodes=[
                NodeConfig('ra1', 'router'),
                NodeConfig('ra2', 'router'),
                NodeConfig('ra3', 'router'),
            ],
            intra_links=[
                LinkConfig('ra1', 'ra3', 'ra1-eth2', 'ra3-eth0', '192.168.1.0/30', '192.168.1.1', '192.168.1.2'),
                LinkConfig('ra2', 'ra3', 'ra2-eth1', 'ra3-eth1', '192.168.1.4/30', '192.168.1.6', '192.168.1.5'),
                LinkConfig('ra1', 'ra2', 'ra1-eth3', 'ra2-eth0', '192.168.1.8/30', '192.168.1.9', '192.168.1.10'),
            ]
        ),
        'AS2': ASConfig(
            as_number='AS2',
            as_type='core',
            nodes=[
                NodeConfig('rb1', 'router'),
                NodeConfig('rb2', 'router'),
                NodeConfig('rb3', 'router'),
            ],
            intra_links=[
                LinkConfig('rb1', 'rb3', 'rb1-eth2', 'rb3-eth0', '192.168.2.0/30', '192.168.2.1', '192.168.2.2'),
                LinkConfig('rb2', 'rb3', 'rb2-eth1', 'rb3-eth1', '192.168.2.4/30', '192.168.2.6', '192.168.2.5'),
                LinkConfig('rb1', 'rb2', 'rb1-eth3', 'rb2-eth0', '192.168.2.8/30', '192.168.2.9', '192.168.2.10'),
            ]
        ),
        'AS3': ASConfig(
            as_number='AS3',
            as_type='core',
            nodes=[
                NodeConfig('rc1', 'router'),
                NodeConfig('rc2', 'router'),
                NodeConfig('rc3', 'router'),
            ],
            intra_links=[
                LinkConfig('rc1', 'rc3', 'rc1-eth4', 'rc3-eth0', '192.168.3.0/30', '192.168.3.1', '192.168.3.2'),
                LinkConfig('rc2', 'rc3', 'rc2-eth1', 'rc3-eth1', '192.168.3.4/30', '192.168.3.6', '192.168.3.5'),
                LinkConfig('rc1', 'rc2', 'rc1-eth3', 'rc2-eth0', '192.168.3.8/30', '192.168.3.9', '192.168.3.10'),
            ]
        ),
        'AS100': ASConfig(
            as_number='AS100',
            as_type='access',
            nodes=[
                NodeConfig('rx', 'router'),
                NodeConfig('x', 'host', default_route='192.168.100.1'),
            ],
            host_networks=[
                NetworkConfig('192.168.100.0/24', '192.168.100.2', '192.168.100.1', 'rx-eth2'),
            ]
        ),
        'AS150': ASConfig(
            as_number='AS150',
            as_type='access',
            nodes=[
                NodeConfig('ry', 'router'),
                NodeConfig('y', 'host', default_route='192.168.150.1'),
            ],
            host_networks=[
                NetworkConfig('192.168.150.0/24', '192.168.150.2', '192.168.150.1', 'ry-eth1'),
            ]
        ),
        'AS200': ASConfig(
            as_number='AS200',
            as_type='access',
            nodes=[
                NodeConfig('rw', 'router'),
                NodeConfig('w', 'host', default_route='192.168.200.1'),
            ],
            host_networks=[
                NetworkConfig('192.168.200.0/24', '192.168.200.2', '192.168.200.1', 'rw-eth1'),
            ]
        ),
    },
    inter_as_links=[
        LinkConfig('ra1', 'rc1', 'ra1-eth0', 'rc1-eth0', '10.0.0.0/30', '10.0.0.1', '10.0.0.2'),
        LinkConfig('ra1', 'rb1', 'ra1-eth1', 'rb1-eth0', '10.0.0.4/30', '10.0.0.5', '10.0.0.6'),
        LinkConfig('rb1', 'rx', 'rb1-eth1', 'rx-eth0', '10.0.0.8/30', '10.0.0.9', '10.0.0.10'),
        LinkConfig('rc1', 'rx', 'rc1-eth1', 'rx-eth1', '10.0.0.12/30', '10.0.0.14', '10.0.0.13'),
        LinkConfig('rc1', 'ry', 'rc1-eth2', 'ry-eth0', '10.0.0.16/30', '10.0.0.17', '10.0.0.18'),
        LinkConfig('ra1', 'rw', 'ra1-eth4', 'rw-eth0', '10.0.0.24/30', '10.0.0.25', '10.0.0.26'),
    ]
) 