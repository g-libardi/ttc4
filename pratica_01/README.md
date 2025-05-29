# Prática 1: Roteamento Inter- e Intra-AS com BGP

Este projeto implementa uma topologia de rede BGP completa usando Mininet, demonstrando conceitos de roteamento inter-AS e intra-AS através de três deliverables progressivos.

## Topologia da Rede

A topologia implementa o seguinte cenário:
- **AS1, AS2, AS3**: Redes core com 3 roteadores cada (usando OSPF internamente)
- **AS100, AS150, AS200**: Redes de acesso com 1 roteador cada
- **Hosts**: x (AS100), y (AS150), w (AS200)

### Esquema de Endereçamento IP

**Links Inter-AS (BGP):**
- AS1-AS3: 10.0.0.0/30 (ra1: .1, rc1: .2)
- AS1-AS2: 10.0.0.4/30 (ra1: .5, rb1: .6)
- AS2-AS100: 10.0.0.8/30 (rb1: .9, rx: .10)
- AS3-AS100: 10.0.0.12/30 (rc1: .13, rx: .14)
- AS3-AS150: 10.0.0.16/30 (rc1: .17, ry: .18)
- AS1-AS200: 10.0.0.24/30 (ra1: .25, rw: .26)

**Links Intra-AS (OSPF/RIP):**
- AS1: 192.168.1.x/30
- AS2: 192.168.2.x/30
- AS3: 192.168.3.x/30

**Redes dos Hosts:**
- AS100: 192.168.100.0/24 (host x: .2, gateway: .1)
- AS150: 192.168.150.0/24 (host y: .2, gateway: .1)
- AS200: 192.168.200.0/24 (host w: .2, gateway: .1)

## Deliverables

### Item 1: Topologia Básica (`item1_topologia_basica.py`)

**Objetivo**: Implementar a topologia física e configuração IP básica.

**Funcionalidades**:
- Criação de todos os roteadores e hosts
- Configuração de endereços IP em todas as interfaces
- Teste de conectividade entre roteadores adjacentes
- Demonstração da topologia física funcionando

**Como executar**:
```bash
# Iniciar a VM
cd ../vm
./run-vn.sh

# Dentro da VM
cd /mnt/hostshare
sudo uv run item1_topologia_basica.py
```

**O que testar no CLI**:
```bash
# Verificar conectividade entre roteadores adjacentes
ra1 ping 10.0.0.2  # ra1 -> rc1 (AS1 -> AS3)
ra1 ping 10.0.0.6  # ra1 -> rb1 (AS1 -> AS2)

# Verificar interfaces configuradas
ra1 ip addr show
rc1 ip addr show

# Tentar ping entre hosts (falhará - sem roteamento)
x ping y  # Falhará - demonstra necessidade de roteamento
```

### Item 2: Roteamento (`item2_roteamento.py`)

**Objetivo**: Adicionar roteamento estático simulando OSPF intra-AS e BGP inter-AS.

**Funcionalidades**:
- Todas as funcionalidades do Item 1
- Configuração de rotas estáticas intra-AS (simulando OSPF)
- Configuração de rotas estáticas inter-AS (simulando BGP)
- Conectividade completa entre todos os hosts
- Análise de tabelas de roteamento

**Como executar**:
```bash
sudo uv run item2_roteamento.py
```

**O que testar no CLI**:
```bash
# Testar conectividade completa
pingall  # Deve funcionar entre todos os nós

# Verificar tabelas de roteamento
ra1 ip route
rb1 ip route
rc1 ip route

# Testar conectividade específica entre hosts
x ping y  # AS100 -> AS150
x ping w  # AS100 -> AS200
y ping w  # AS150 -> AS200

# Verificar caminhos com traceroute
x traceroute 192.168.150.2  # Caminho de x para y
```

### Item 3: Filtros BGP (`item3_filtros_bgp.py`)

**Objetivo**: Demonstrar problemas de roteamento BGP e implementar filtros.

**Funcionalidades**:
- Todas as funcionalidades do Item 2
- Demonstração do problema: AS100 sendo usado como trânsito
- Implementação de filtros BGP para corrigir o problema
- Comparação antes/depois dos filtros
- Análise detalhada de caminhos de roteamento

**Como executar**:
```bash
sudo uv run item3_filtros_bgp.py
```

**O que testar no CLI**:
```bash
# O script automaticamente demonstra:
# 1. Problema: tráfego AS150->AS1 passando por AS100
# 2. Solução: filtros BGP impedindo uso incorreto de AS100

# Verificar tabelas de roteamento após filtros
ra1 ip route
rc1 ip route
ry ip route

# Testar caminhos corrigidos
y traceroute 1.1.1.1  # Deve ir direto AS150->AS3->AS1
```

## Conceitos Demonstrados

### Item 1: Fundamentos de Rede
- Topologia física de rede
- Configuração de interfaces IP
- Conectividade básica entre roteadores
- Segmentação de redes por AS

### Item 2: Protocolos de Roteamento
- **OSPF Intra-AS**: Roteamento dentro de cada AS
- **BGP Inter-AS**: Roteamento entre diferentes ASes
- Tabelas de roteamento completas
- Conectividade end-to-end

### Item 3: Políticas BGP
- **Problema de Trânsito**: AS de acesso usado incorretamente
- **Filtros BGP**: Prevenção de uso inadequado de rotas
- **Políticas de Roteamento**: Controle de tráfego entre ASes
- **Análise de Caminhos**: Verificação de rotas corretas

## Requisitos

- VM NixOS configurada (diretório `../vm/`)
- UV package manager (já configurado na VM)
- Mininet (já instalado na VM)
- Privilégios de root (sudo)

## Estrutura dos Arquivos

```
pratica_01/
├── README.md                    # Este arquivo
├── INSTRUCOES_EXECUCAO.md      # Instruções detalhadas
├── item1_topologia_basica.py    # Deliverable 1: Topologia básica
├── item2_roteamento.py          # Deliverable 2: Roteamento completo
├── item3_filtros_bgp.py         # Deliverable 3: Filtros BGP
├── test_vm_execution.py         # Script de teste do ambiente
├── pyproject.toml               # Configuração UV
└── uv.lock                      # Lock file UV
```

## Comandos Úteis no Mininet CLI

```bash
# Conectividade
pingall                          # Testa conectividade entre todos os nós
x ping y                         # Ping específico entre hosts

# Roteamento
ra1 ip route                     # Tabela de roteamento do ra1
ra1 ip route show table main     # Tabela principal de roteamento

# Análise de rede
x traceroute 192.168.150.2       # Traça caminho de x para y
ra1 ip addr show                 # Mostra interfaces do ra1

# Debugging
ra1 ping -c 3 10.0.0.2          # Ping com contagem específica
nodes                            # Lista todos os nós
links                            # Lista todos os links
```

## Execução Passo a Passo

### 1. Preparar o Ambiente
```bash
# Navegar para o diretório da VM
cd ../vm

# Iniciar a VM
./run-vn.sh
```

### 2. Dentro da VM
```bash
# Login: user / senha: pass

# Navegar para o diretório compartilhado
cd /mnt/hostshare

# Testar o ambiente (opcional)
uv run test_vm_execution.py

# Executar o Item 1
sudo uv run item1_topologia_basica.py
```

### 3. No CLI do Mininet
```bash
# Testar conectividade básica
ra1 ping 10.0.0.2
ra1 ping 10.0.0.6

# Verificar configuração
ra1 ip addr show
pingall  # Falhará - demonstra necessidade de roteamento

# Sair do CLI
exit
```

## Observações Importantes

1. **UV Package Manager**: A VM usa UV para gerenciar dependências Python
2. **Execução**: Todos os scripts devem ser executados com `sudo uv run`
3. **Ordem**: Execute os itens em sequência para melhor compreensão
4. **CLI**: Use o CLI do Mininet para explorar e testar a rede
5. **Limpeza**: Use `sudo mn -c` entre execuções para limpar o ambiente

## Troubleshooting

**Problema**: "Permission denied" ou "Command not found"
**Solução**: Execute com `sudo uv run` e verifique se está na VM

**Problema**: Conectividade falha entre hosts
**Solução**: Verifique se as rotas estão configuradas corretamente com `ip route`

**Problema**: Interface não encontrada
**Solução**: Verifique se a topologia foi criada corretamente e as interfaces existem

**Problema**: UV não encontrado
**Solução**: Certifique-se de estar executando dentro da VM NixOS
