#!/usr/bin/env python3
"""
Item 1: Implementação da Topologia Básica
Prática 1 - TTC4 - Roteamento Inter-AS e Intra-AS com BGP

This file now uses the modular implementation for better organization and maintainability.
The original monolithic code has been refactored into separate modules:

- config.py: Configuration dataclasses and topology definition
- topology.py: Mininet topology creation  
- network.py: Network configuration and setup
- testing.py: Connectivity testing functions
- utils.py: Utility functions and displays
- main.py: Main entry point and CLI

Topologia:
- AS1 (rede a): ra1, ra2, ra3 - Core network
- AS2 (rede b): rb1, rb2, rb3 - Core network  
- AS3 (rede c): rc1, rc2, rc3 - Core network
- AS100 (rede x): rx + host x - Access network
- AS150 (rede y): ry + host y - Access network
- AS200 (rede w): rw + host w - Access network
"""

# Import the main function from the modular implementation
from main import run_topology

# Keep original entry point for backward compatibility
if __name__ == '__main__':
    run_topology() 