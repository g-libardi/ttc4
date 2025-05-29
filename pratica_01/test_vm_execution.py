#!/usr/bin/env python3
"""
Script de teste para verificar se o ambiente da VM está funcionando
"""

import sys
import os

def test_imports():
    """Testa se as importações necessárias estão disponíveis"""
    try:
        from mininet.net import Mininet
        from mininet.node import Node
        from mininet.link import TCLink
        from mininet.log import setLogLevel, info
        from mininet.cli import CLI
        from mininet.topo import Topo
        print("✓ Todas as importações do Mininet estão disponíveis")
        return True
    except ImportError as e:
        print(f"✗ Erro de importação: {e}")
        return False

def test_topology_creation():
    """Testa se conseguimos criar uma topologia básica"""
    try:
        # Importar nossa topologia
        from item1_topologia_basica import BGPTopology, LinuxRouter
        
        # Criar topologia
        topo = BGPTopology()
        print("✓ Topologia BGP criada com sucesso")
        
        # Verificar nós
        nodes = list(topo.nodes())
        print(f"✓ {len(nodes)} nós criados: {nodes}")
        
        # Verificar links
        links = list(topo.links())
        print(f"✓ {len(links)} links criados")
        
        return True
    except Exception as e:
        print(f"✗ Erro na criação da topologia: {e}")
        return False

def main():
    print("=== Teste do Ambiente VM ===\n")
    
    print("1. Testando importações...")
    imports_ok = test_imports()
    
    print("\n2. Testando criação da topologia...")
    topology_ok = test_topology_creation()
    
    print(f"\n=== Resultado ===")
    if imports_ok and topology_ok:
        print("✓ Ambiente está funcionando corretamente!")
        print("✓ Pronto para executar: sudo uv run item1_topologia_basica.py")
        return 0
    else:
        print("✗ Há problemas no ambiente")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 