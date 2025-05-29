#!/usr/bin/env python3
"""
Item 1: Implementação da Topologia Básica
Prática 1 - TTC4 - Roteamento Inter-AS e Intra-AS com BGP

Topologia:
- AS1 (rede a): ra1, ra2, ra3 - Core network
- AS2 (rede b): rb1, rb2, rb3 - Core network  
- AS3 (rede c): rc1, rc2, rc3 - Core network
- AS100 (rede x): rx + host x - Access network
- AS150 (rede y): ry + host y - Access network
- AS200 (rede w): rw + host w - Access network
"""

from mininet.net import Mininet
from mininet.node import Node, RemoteController
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.topo import Topo
import time

class LinuxRouter(Node):
    """Um nó Linux que pode atuar como roteador"""
    
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Habilita forwarding IP
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetTopo(Topo):
    """Topologia BGP com múltiplos AS"""
    
    def build(self):
        # Criar roteadores para cada AS
        
        # AS1 (rede a) - Core
        ra1 = self.addNode('ra1', cls=LinuxRouter, ip=None)
        ra2 = self.addNode('ra2', cls=LinuxRouter, ip=None)
        ra3 = self.addNode('ra3', cls=LinuxRouter, ip=None)
        
        # AS2 (rede b) - Core
        rb1 = self.addNode('rb1', cls=LinuxRouter, ip=None)
        rb2 = self.addNode('rb2', cls=LinuxRouter, ip=None)
        rb3 = self.addNode('rb3', cls=LinuxRouter, ip=None)
        
        # AS3 (rede c) - Core
        rc1 = self.addNode('rc1', cls=LinuxRouter, ip=None)
        rc2 = self.addNode('rc2', cls=LinuxRouter, ip=None)
        rc3 = self.addNode('rc3', cls=LinuxRouter, ip=None)
        
        # AS100 (rede x) - Access
        rx = self.addNode('rx', cls=LinuxRouter, ip=None)
        
        # AS150 (rede y) - Access
        ry = self.addNode('ry', cls=LinuxRouter, ip=None)
        
        # AS200 (rede w) - Access
        rw = self.addNode('rw', cls=LinuxRouter, ip=None)
        
        # Hosts
        x = self.addHost('x', ip='192.168.100.2/24', defaultRoute='via 192.168.100.1')
        y = self.addHost('y', ip='192.168.150.2/24', defaultRoute='via 192.168.150.1')
        w = self.addHost('w', ip='192.168.200.2/24', defaultRoute='via 192.168.200.1')
        
        # Links Intra-AS
        
        # AS1 - Topologia triangular (conforme diagrama)
        self.addLink(ra1, ra3, intfName1='ra1-eth2', intfName2='ra3-eth0')  # 192.168.1.0/30
        self.addLink(ra2, ra3, intfName1='ra2-eth1', intfName2='ra3-eth1')  # 192.168.1.4/30  
        self.addLink(ra1, ra2, intfName1='ra1-eth3', intfName2='ra2-eth0')  # 192.168.1.8/30
        
        # AS2 - Topologia triangular (conforme diagrama)
        self.addLink(rb1, rb3, intfName1='rb1-eth2', intfName2='rb3-eth0')  # 192.168.2.0/30
        self.addLink(rb2, rb3, intfName1='rb2-eth1', intfName2='rb3-eth1')  # 192.168.2.4/30
        self.addLink(rb1, rb2, intfName1='rb1-eth3', intfName2='rb2-eth0')  # 192.168.2.8/30
        
        # AS3 - Topologia triangular (conforme diagrama)
        self.addLink(rc1, rc3, intfName1='rc1-eth3', intfName2='rc3-eth0')  # 192.168.3.0/30
        self.addLink(rc2, rc3, intfName1='rc2-eth1', intfName2='rc3-eth1')  # 192.168.3.4/30
        self.addLink(rc1, rc2, intfName1='rc1-eth4', intfName2='rc2-eth0')  # 192.168.3.8/30
        
        # Links Inter-AS (BGP) - conforme diagrama
        self.addLink(ra1, rc1, intfName1='ra1-eth0', intfName2='rc1-eth0')  # 10.0.0.0/30
        self.addLink(ra1, rb1, intfName1='ra1-eth1', intfName2='rb1-eth0')  # 10.0.0.4/30
        self.addLink(rb1, rx, intfName1='rb1-eth1', intfName2='rx-eth0')    # 10.0.0.8/30
        self.addLink(rc1, rx, intfName1='rc1-eth1', intfName2='rx-eth1')    # 10.0.0.12/30
        self.addLink(rc1, ry, intfName1='rc1-eth2', intfName2='ry-eth0')    # 10.0.0.16/30
        self.addLink(ra1, rw, intfName1='ra1-eth4', intfName2='rw-eth0')    # 10.0.0.24/30
        
        # Links para hosts (conforme diagrama)
        self.addLink(rx, x, intfName1='rx-eth2', intfName2='x-eth0')        # 192.168.100.0/24
        self.addLink(ry, y, intfName1='ry-eth1', intfName2='y-eth0')        # 192.168.150.0/24
        self.addLink(rw, w, intfName1='rw-eth1', intfName2='w-eth0')        # 192.168.200.0/24

def configure_network(net):
    """Configura endereços IP em todas as interfaces"""
    
    info('*** Configurando endereços IP...\n')
    
    # Obter referências dos nós
    ra1, ra2, ra3 = net.get('ra1', 'ra2', 'ra3')
    rb1, rb2, rb3 = net.get('rb1', 'rb2', 'rb3')
    rc1, rc2, rc3 = net.get('rc1', 'rc2', 'rc3')
    rx, ry, rw = net.get('rx', 'ry', 'rw')
    
    # Configurar AS1 (192.168.1.x/30) - conforme diagrama
    info('*** Configurando AS1...\n')
    ra1.cmd('ip addr add 192.168.1.1/30 dev ra1-eth2')   # ra1-ra3 (e2:1)
    ra3.cmd('ip addr add 192.168.1.2/30 dev ra3-eth0')   # ra3-ra1 (e0:2)
    
    ra2.cmd('ip addr add 192.168.1.5/30 dev ra2-eth1')   # ra2-ra3 (e1:5)
    ra3.cmd('ip addr add 192.168.1.6/30 dev ra3-eth1')   # ra3-ra2 (e1:6)
    
    ra1.cmd('ip addr add 192.168.1.9/30 dev ra1-eth3')   # ra1-ra2 (e3:9)
    ra2.cmd('ip addr add 192.168.1.10/30 dev ra2-eth0')  # ra2-ra1 (e0:10)
    
    # Configurar AS2 (192.168.2.x/30) - conforme diagrama
    info('*** Configurando AS2...\n')
    rb1.cmd('ip addr add 192.168.2.1/30 dev rb1-eth2')   # rb1-rb3 (e2:1)
    rb3.cmd('ip addr add 192.168.2.2/30 dev rb3-eth0')   # rb3-rb1 (e0:2)
    
    rb2.cmd('ip addr add 192.168.2.5/30 dev rb2-eth1')   # rb2-rb3 (e1:5)
    rb3.cmd('ip addr add 192.168.2.6/30 dev rb3-eth1')   # rb3-rb2 (e1:6)
    
    rb1.cmd('ip addr add 192.168.2.9/30 dev rb1-eth3')   # rb1-rb2 (e3:9)
    rb2.cmd('ip addr add 192.168.2.10/30 dev rb2-eth0')  # rb2-rb1 (e0:10)
    
    # Configurar AS3 (192.168.3.x/30) - conforme diagrama
    info('*** Configurando AS3...\n')
    rc1.cmd('ip addr add 192.168.3.1/30 dev rc1-eth3')   # rc1-rc3 (e3:1)
    rc3.cmd('ip addr add 192.168.3.2/30 dev rc3-eth0')   # rc3-rc1 (e0:2)
    
    rc2.cmd('ip addr add 192.168.3.5/30 dev rc2-eth1')   # rc2-rc3 (e1:5)
    rc3.cmd('ip addr add 192.168.3.6/30 dev rc3-eth1')   # rc3-rc2 (e1:6)
    
    rc1.cmd('ip addr add 192.168.3.9/30 dev rc1-eth4')   # rc1-rc2 (e4:9)
    rc2.cmd('ip addr add 192.168.3.10/30 dev rc2-eth0')  # rc2-rc1 (e0:10)
    
    # Configurar links Inter-AS (10.0.0.x/30) - conforme diagrama
    info('*** Configurando links Inter-AS...\n')
    ra1.cmd('ip addr add 10.0.0.1/30 dev ra1-eth0')      # AS1-AS3 (e0:1)
    rc1.cmd('ip addr add 10.0.0.2/30 dev rc1-eth0')      # AS3-AS1 (e0:2)
    
    ra1.cmd('ip addr add 10.0.0.5/30 dev ra1-eth1')      # AS1-AS2 (e1:5)
    rb1.cmd('ip addr add 10.0.0.6/30 dev rb1-eth0')      # AS2-AS1 (e0:6)
    
    rb1.cmd('ip addr add 10.0.0.9/30 dev rb1-eth1')      # AS2-AS100 (e1:9)
    rx.cmd('ip addr add 10.0.0.10/30 dev rx-eth0')       # AS100-AS2 (e0:10)
    
    rc1.cmd('ip addr add 10.0.0.13/30 dev rc1-eth1')     # AS3-AS100 (e1:13)
    rx.cmd('ip addr add 10.0.0.14/30 dev rx-eth1')       # AS100-AS3 (e1:14)
    
    rc1.cmd('ip addr add 10.0.0.17/30 dev rc1-eth2')     # AS3-AS150 (e2:17)
    ry.cmd('ip addr add 10.0.0.18/30 dev ry-eth0')       # AS150-AS3 (e0:18)
    
    ra1.cmd('ip addr add 10.0.0.25/30 dev ra1-eth4')     # AS1-AS200 (e4:25)
    rw.cmd('ip addr add 10.0.0.26/30 dev rw-eth0')       # AS200-AS1 (e0:26)
    
    # Configurar redes dos hosts - conforme diagrama
    info('*** Configurando redes dos hosts...\n')
    rx.cmd('ip addr add 192.168.100.1/24 dev rx-eth2')   # Gateway AS100 (e2:1)
    ry.cmd('ip addr add 192.168.150.1/24 dev ry-eth1')   # Gateway AS150 (e1:1)
    rw.cmd('ip addr add 192.168.200.1/24 dev rw-eth1')   # Gateway AS200 (e1:1)
    
    # Aguardar configuração
    time.sleep(2)

def test_basic_connectivity(net):
    """Testa conectividade básica entre roteadores adjacentes"""
    
    info('*** Testando conectividade básica...\n')
    
    # Obter referências dos nós
    ra1, rb1, rc1 = net.get('ra1', 'rb1', 'rc1')
    rx, ry, rw = net.get('rx', 'ry', 'rw')
    x, y, w = net.get('x', 'y', 'w')
    
    # Testes de conectividade entre roteadores adjacentes
    tests = [
        (ra1, '10.0.0.2', 'AS1 -> AS3 (ra1 -> rc1)'),
        (ra1, '10.0.0.6', 'AS1 -> AS2 (ra1 -> rb1)'),
        (rb1, '10.0.0.10', 'AS2 -> AS100 (rb1 -> rx)'),
        (rc1, '10.0.0.14', 'AS3 -> AS100 (rc1 -> rx)'),
        (rc1, '10.0.0.18', 'AS3 -> AS150 (rc1 -> ry)'),
        (ra1, '10.0.0.26', 'AS1 -> AS200 (ra1 -> rw)'),
    ]
    
    info('=== Testes de Conectividade Inter-AS ===\n')
    for router, target_ip, description in tests:
        result = router.cmd(f'ping -c 1 -W 2 {target_ip}')
        if '1 received' in result:
            info(f'✓ {description}: OK\n')
        else:
            info(f'✗ {description}: FALHOU\n')
    
    # Teste de conectividade intra-AS (AS1)
    info('\n=== Testes de Conectividade Intra-AS (AS1) ===\n')
    ra2, ra3 = net.get('ra2', 'ra3')
    intra_tests = [
        (ra1, '192.168.1.2', 'ra1 -> ra3'),
        (ra1, '192.168.1.10', 'ra1 -> ra2'),
        (ra2, '192.168.1.6', 'ra2 -> ra3'),
    ]
    
    for router, target_ip, description in intra_tests:
        result = router.cmd(f'ping -c 1 -W 2 {target_ip}')
        if '1 received' in result:
            info(f'✓ {description}: OK\n')
        else:
            info(f'✗ {description}: FALHOU\n')
    
    # Teste de conectividade com hosts (deve falhar - sem roteamento)
    info('\n=== Testes de Conectividade com Hosts (esperado falhar) ===\n')
    host_tests = [
        (x, '192.168.150.2', 'host x -> host y'),
        (x, '192.168.200.2', 'host x -> host w'),
        (y, '192.168.200.2', 'host y -> host w'),
    ]
    
    for host, target_ip, description in host_tests:
        result = host.cmd(f'ping -c 1 -W 2 {target_ip}')
        if '1 received' in result:
            info(f'✓ {description}: OK (inesperado!)\n')
        else:
            info(f'✗ {description}: FALHOU (esperado - sem roteamento)\n')

def show_network_info(net):
    """Mostra informações da rede configurada"""
    
    info('\n*** Informações da Rede ***\n')
    
    # Mostrar interfaces de alguns roteadores principais
    routers_to_show = ['ra1', 'rb1', 'rc1', 'rx', 'ry', 'rw']
    
    for router_name in routers_to_show:
        router = net.get(router_name)
        info(f'\n=== {router_name.upper()} ===\n')
        result = router.cmd('ip addr show | grep -E "(inet |^[0-9]+:)"')
        info(result)

def run_topology():
    """Função principal para executar a topologia"""
    
    setLogLevel('info')
    
    info('*** Criando topologia BGP ***\n')
    topo = NetTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    
    info('*** Iniciando rede ***\n')
    net.start()
    
    # Configurar endereços IP
    configure_network(net)
    
    # Mostrar informações da rede
    show_network_info(net)
    
    # Testar conectividade básica
    test_basic_connectivity(net)
    
    info('\n*** Rede configurada! ***\n')
    info('*** Use os seguintes comandos para testar: ***\n')
    info('  pingall                    # Testa conectividade (falhará - sem roteamento)\n')
    info('  ra1 ping 10.0.0.2         # Teste AS1 -> AS3\n')
    info('  ra1 ping 10.0.0.6         # Teste AS1 -> AS2\n')
    info('  ra1 ip addr show          # Mostra interfaces do ra1\n')
    info('  ra1 ip route              # Mostra tabela de roteamento\n')
    info('  x ping y                  # Teste entre hosts (falhará)\n')
    info('\n*** Iniciando CLI do Mininet ***\n')
    
    CLI(net)
    
    info('*** Parando rede ***\n')
    net.stop()

if __name__ == '__main__':
    run_topology() 