#!/usr/bin/env python3
"""
Testing module for BGP network
Contains functions for testing basic connectivity between nodes
"""

from mininet.net import Mininet
from mininet.log import info
from .config import TOPOLOGY


def test_basic_connectivity(net: Mininet) -> None:
    """Testa conectividade básica entre roteadores adjacentes"""
    
    info('*** Testando conectividade básica ***\n')
    
    # Test inter-AS connectivity
    _test_inter_as_connectivity(net)
    
    # Test intra-AS connectivity (AS1 example)
    _test_intra_as_connectivity(net)
    
    # Test host connectivity (should fail - no routing)
    _test_host_connectivity(net)


def _test_inter_as_connectivity(net: Mininet) -> None:
    """Test connectivity between adjacent AS routers"""
    info('=== Testes de Conectividade Inter-AS ===\n')
    
    for link in TOPOLOGY.inter_as_links:
        router = net.get(link.node1)
        result = router.cmd(f'ping -c 1 -W 2 {link.ip2}')
        description = f'{link.node1} -> {link.node2}'
        
        if '1 received' in result:
            info(f'✓ {description}: OK\n')
        else:
            info(f'✗ {description}: FALHOU\n')


def _test_intra_as_connectivity(net: Mininet) -> None:
    """Test connectivity within AS1 as example"""
    info('\n=== Testes de Conectividade Intra-AS (AS1) ===\n')
    
    as1_config = TOPOLOGY.autonomous_systems['AS1']
    
    for link in as1_config.intra_links:
        router = net.get(link.node1)
        result = router.cmd(f'ping -c 1 -W 2 {link.ip2}')
        description = f'{link.node1} -> {link.node2}'
        
        if '1 received' in result:
            info(f'✓ {description}: OK\n')
        else:
            info(f'✗ {description}: FALHOU\n')


def _test_host_connectivity(net: Mininet) -> None:
    """Test connectivity between hosts (should fail - no routing)"""
    info('\n=== Testes de Conectividade com Hosts (esperado falhar) ===\n')
    
    # Get all access ASes and their host configurations
    access_ases = TOPOLOGY.get_access_ases()
    host_configs = []
    
    for as_config in access_ases.values():
        host_name = as_config.get_hosts()[0]
        host_ip = as_config.host_networks[0].host_ip
        host_configs.append((host_name, host_ip))
    
    # Test connectivity between different hosts
    test_cases = [
        (host_configs[0][0], host_configs[1][1], f"host {host_configs[0][0]} -> host {host_configs[1][0]}"),
        (host_configs[0][0], host_configs[2][1], f"host {host_configs[0][0]} -> host {host_configs[2][0]}"),
        (host_configs[1][0], host_configs[2][1], f"host {host_configs[1][0]} -> host {host_configs[2][0]}"),
    ]
    
    for host_name, target_ip, description in test_cases:
        host = net.get(host_name)
        result = host.cmd(f'ping -c 1 -W 2 {target_ip}')
        if '1 received' in result:
            info(f'✓ {description}: OK (inesperado!)\n')
        else:
            info(f'✗ {description}: FALHOU (esperado - sem roteamento)\n') 