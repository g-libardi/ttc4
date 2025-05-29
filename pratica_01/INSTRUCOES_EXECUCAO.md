# Instruções para Execução do Item 1 - Topologia Básica

## Pré-requisitos

Este projeto requer execução em uma VM com Mininet instalado. A VM está configurada no diretório `../vm/` e usa o UV package manager.

## Como Executar

### 1. Iniciar a VM

```bash
cd ../vm
./run-vn.sh
```

### 2. Dentro da VM

Após a VM inicializar, você estará logado como usuário `user` (senha: `pass`).

```bash
# Navegar para o diretório compartilhado
cd /mnt/hostshare

# Executar o Item 1 usando UV
sudo uv run item1_topologia_basica.py
```

## O que o Item 1 Implementa

### Topologia Criada

**AS Core (3 roteadores cada):**
- **AS1**: ra1, ra2, ra3 (rede a)
- **AS2**: rb1, rb2, rb3 (rede b)  
- **AS3**: rc1, rc2, rc3 (rede c)

**AS Access (1 roteador + 1 host cada):**
- **AS100**: rx + host x (rede x)
- **AS150**: ry + host y (rede y)
- **AS200**: rw + host w (rede w)

### Esquema de Endereçamento

**Links Inter-AS (BGP):**
```
AS1-AS3:  10.0.0.0/30   (ra1: .1, rc1: .2)
AS1-AS2:  10.0.0.4/30   (ra1: .5, rb1: .6)
AS2-AS100: 10.0.0.8/30  (rb1: .9, rx: .10)
AS3-AS100: 10.0.0.12/30 (rc1: .13, rx: .14)
AS3-AS150: 10.0.0.16/30 (rc1: .17, ry: .18)
AS1-AS200: 10.0.0.24/30 (ra1: .25, rw: .26)
```

**Links Intra-AS (OSPF):**
```
AS1: 192.168.1.x/30
AS2: 192.168.2.x/30
AS3: 192.168.3.x/30
```

**Redes dos Hosts:**
```
AS100: 192.168.100.0/24 (host x: .2, gateway: .1)
AS150: 192.168.150.0/24 (host y: .2, gateway: .1)
AS200: 192.168.200.0/24 (host w: .2, gateway: .1)
```

## Testes Automáticos

O script executa automaticamente os seguintes testes:

1. **Conectividade Inter-AS**: Ping entre roteadores adjacentes
2. **Conectividade Intra-AS**: Ping dentro do AS1
3. **Conectividade entre Hosts**: Deve falhar (sem roteamento)

## Comandos para Testar no CLI do Mininet

Após a execução, você estará no CLI do Mininet. Use estes comandos:

### Testes Básicos
```bash
# Verificar conectividade (falhará - sem roteamento)
pingall

# Ping específico entre roteadores adjacentes
ra1 ping 10.0.0.2    # AS1 -> AS3
ra1 ping 10.0.0.6    # AS1 -> AS2
rb1 ping 10.0.0.10   # AS2 -> AS100
```

### Verificar Configuração
```bash
# Mostrar interfaces configuradas
ra1 ip addr show
rc1 ip addr show
rx ip addr show

# Mostrar tabela de roteamento (vazia neste item)
ra1 ip route
```

### Testes entre Hosts (Falharão)
```bash
# Estes comandos falharão pois não há roteamento configurado
x ping y    # AS100 -> AS150
x ping w    # AS100 -> AS200
y ping w    # AS150 -> AS200
```

## Resultados Esperados

### ✅ Deve Funcionar
- Ping entre roteadores diretamente conectados
- Configuração de interfaces IP
- Conectividade física da rede

### ❌ Deve Falhar (Esperado)
- Ping entre hosts de diferentes AS
- Comando `pingall` (conectividade completa)
- Roteamento entre redes não adjacentes

## Próximos Passos

O **Item 2** adicionará roteamento estático para permitir conectividade completa entre todos os hosts.

## Troubleshooting

### VM não inicia
```bash
cd ../vm
./build-vm.sh  # Reconstrói a VM se necessário
```

### Erro de permissão no Mininet
```bash
# Certifique-se de usar sudo com uv
sudo uv run item1_topologia_basica.py
```

### Interface não encontrada
- Verifique se a topologia foi criada corretamente
- Use `nodes` e `links` no CLI para verificar a estrutura

### Limpeza entre execuções
```bash
# Limpar configuração anterior do Mininet
sudo mn -c
```

## Comandos Alternativos

Se houver problemas com UV, você também pode executar diretamente:
```bash
# Alternativa sem UV (se python3 estiver disponível)
sudo python3 item1_topologia_basica.py
``` 