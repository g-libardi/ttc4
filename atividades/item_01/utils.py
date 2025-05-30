#!/usr/bin/env python3
"""
Utilities module for BGP network
Contains helper functions for displaying configuration summaries and other utilities
"""

from mininet.log import info
from .config import TOPOLOGY


def show_configuration_summary() -> None:
    """Show a summary of the unified configuration"""
    info('\n*** Resumo da Configuração Unificada ***\n')
    
    # Show AS information
    info('=== Autonomous Systems ===\n')
    for as_name, as_config in TOPOLOGY.autonomous_systems.items():
        routers = as_config.get_routers()
        hosts = as_config.get_hosts()
        info(f'{as_name} ({as_config.as_type}): ')
        if routers:
            info(f'routers={", ".join(routers)}')
        if hosts:
            info(f' hosts={", ".join(hosts)}')
        info('\n')
    
    # Show network summary
    info('\n=== Redes Configuradas ===\n')
    info('Inter-AS (BGP):\n')
    for link in TOPOLOGY.inter_as_links:
        info(f'  {link.network}: {link.node1}({link.ip1}) ↔ {link.node2}({link.ip2})\n')
    
    info('\nAccess Networks:\n')
    for as_name, as_config in TOPOLOGY.get_access_ases().items():
        if as_config.host_networks:
            net_config = as_config.host_networks[0]
            info(f'  {as_name}: {net_config.network} (host: {net_config.host_ip}, gw: {net_config.gateway_ip})\n')


def show_usage_instructions() -> None:
    """Show usage instructions for the CLI"""
    info('\n*** Rede configurada! ***\n')
    info('*** Use os seguintes comandos para testar: ***\n')
    info('  pingall                      # Testa conectividade (falhará - sem roteamento)\n')
    info('  ra1 ping 10.0.0.2           # Teste AS1 -> AS3\n')
    info('  ra1 ping 10.0.0.6           # Teste AS1 -> AS2\n')
    info('  ra1 ip addr show            # Mostra interfaces do ra1\n')
    info('  ra1 ip route                # Mostra tabela de roteamento\n')
    info('  x ping 192.168.150.2        # host x -> host y (falhará - sem roteamento)\n')
    info('  x ping 192.168.200.2        # host x -> host w (falhará - sem roteamento)\n')
    info('  nodes                       # Lista todos os nós\n')
    info('  links                       # Lista todos os links\n') 