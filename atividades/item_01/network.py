#!/usr/bin/env python3
"""
Network configuration module
Contains functions for configuring IP addresses, routing, and network setup
"""

import time
from mininet.net import Mininet
from mininet.log import info
from .config import TOPOLOGY


def configure_network(net: Mininet) -> None:
    """Configura endereços IP em todas as interfaces baseado na configuração unificada"""
    
    info('*** Configurando endereços IP...\n')
    
    # Enable IP forwarding for all routers
    _enable_ip_forwarding(net)
    
    # Configure intra-AS links
    _configure_intra_as_links(net)
    
    # Configure inter-AS links
    _configure_inter_as_links(net)
    
    # Configure host networks
    _configure_host_networks(net)
    
    # Wait for configuration to take effect
    info('*** Aguardando configuração de rede ***\n')
    time.sleep(5)


def _enable_ip_forwarding(net: Mininet) -> None:
    """Enable IP forwarding for all router nodes"""
    info('*** Habilitando IP forwarding nos roteadores ***\n')
    
    # Get all router nodes using the unified topology config method
    router_nodes = TOPOLOGY.get_all_router_nodes()
    
    # Enable forwarding
    for router_name in router_nodes:
        router = net.get(router_name)
        router.cmd('sysctl net.ipv4.ip_forward=1')


def _configure_intra_as_links(net: Mininet) -> None:
    """Configure IP addresses for intra-AS links"""
    for as_name, as_config in TOPOLOGY.autonomous_systems.items():
        if as_config.intra_links:
            info(f'*** Configurando {as_name} ***\n')
            for link in as_config.intra_links:
                router1 = net.get(link.node1)
                router2 = net.get(link.node2)
                
                router1.cmd(f'ip addr add {link.ip1}/{link.mask} dev {link.intf1}')
                router2.cmd(f'ip addr add {link.ip2}/{link.mask} dev {link.intf2}')


def _configure_inter_as_links(net: Mininet) -> None:
    """Configure IP addresses for inter-AS links"""
    info('*** Configurando links Inter-AS ***\n')
    for link in TOPOLOGY.inter_as_links:
        router1 = net.get(link.node1)
        router2 = net.get(link.node2)
        
        router1.cmd(f'ip addr add {link.ip1}/{link.mask} dev {link.intf1}')
        router2.cmd(f'ip addr add {link.ip2}/{link.mask} dev {link.intf2}')


def _configure_host_networks(net: Mininet) -> None:
    """Configure host networks and default routes"""
    info('*** Configurando redes dos hosts ***\n')
    for as_name, as_config in TOPOLOGY.autonomous_systems.items():
        if as_config.host_networks:
            router_name = as_config.get_routers()[0]
            host_name = as_config.get_hosts()[0]
            network_config = as_config.host_networks[0]
            
            router = net.get(router_name)
            host = net.get(host_name)
            
            # Configure gateway on router
            router.cmd(f'ip addr add {network_config.gateway_ip}/{network_config.mask} dev {network_config.host_intf}')
            
            # Configure host IP and default route
            host.cmd(f'ip addr add {network_config.host_ip}/{network_config.mask} dev {host_name}-eth0')
            host.cmd(f'ip route add default via {network_config.gateway_ip}') 