#!/usr/bin/env python3
"""
BGP Topology Package
Modular implementation of BGP network topology for TTC4 course

Modules:
- config: Configuration dataclasses and topology definition
- topology: Mininet topology creation
- network: Network configuration and setup
- testing: Connectivity testing functions
- utils: Utility functions and displays
- main: Main entry point and CLI
"""

from .config import TOPOLOGY, TopologyConfig, ASConfig, LinkConfig, NodeConfig, NetworkConfig
from .topology import NetTopo
from .network import configure_network
from .testing import test_basic_connectivity
from .utils import show_configuration_summary, show_usage_instructions

__all__ = [
    'TOPOLOGY',
    'TopologyConfig',
    'ASConfig', 
    'LinkConfig',
    'NodeConfig',
    'NetworkConfig',
    'NetTopo',
    'configure_network',
    'test_basic_connectivity',
    'show_configuration_summary',
    'show_usage_instructions'
] 