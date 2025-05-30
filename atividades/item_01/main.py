#!/usr/bin/env python3
"""
Main module for BGP topology
Main entry point that orchestrates the entire BGP topology setup and execution
"""

import os
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.clean import cleanup

from .topology import NetTopo
from .network import configure_network
from .testing import test_basic_connectivity
from .utils import show_configuration_summary, show_usage_instructions


def run_topology() -> None:
    """Função principal para executar a topologia"""
    
    setLogLevel('info')

    info('*** Limpando ambiente do Mininet ***\n')
    os.system('sudo mn -c')
    
    info('*** Criando topologia BGP ***\n')
    topo = NetTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    
    info('*** Iniciando rede ***\n')
    net.start()
    
    # Show configuration summary
    show_configuration_summary()
    
    # Configure network based on unified config
    configure_network(net)
    
    # Test basic connectivity
    test_basic_connectivity(net)
    
    # Show usage instructions
    show_usage_instructions()
    
    info('\n*** Iniciando CLI do Mininet ***\n')
    
    CLI(net)
    
    info('*** Parando rede ***\n')
    net.stop()
    cleanup()


if __name__ == '__main__':
    run_topology() 