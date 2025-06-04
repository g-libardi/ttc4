# Mininet Vagrant Nix Flake

A Nix flake that provides a complete development environment for running [Mininet experiments using Vagrant](https://github.com/brunokimura-dev/mininet-vagrant). This flake includes all necessary tools and helper scripts to get you started quickly.

## 🚀 Quick Start

### Prerequisites

1. **Nix with flakes enabled** (NixOS or Nix package manager)
2. **Hardware virtualization support** (Intel VT-x or AMD-V)
3. **VirtualBox kernel modules** (handled automatically on NixOS)

### Usage

1. **Enter the development environment:**
   ```bash
   nix develop
   ```

2. **Setup the Mininet Vagrant repository:**
   ```bash
   setup-mininet-vagrant
   ```

3. **Start the Vagrant VM:**
   ```bash
   vagrant-helper up
   ```

4. **Run a Mininet experiment:**
   ```bash
   run-mininet mn-ex-base-1.py
   ```

## 📋 Available Commands

### Setup Commands
- `setup-mininet-vagrant` - Clone and setup the mininet-vagrant repository
- `vagrant-helper <cmd>` - Helper for common Vagrant operations

### Vagrant Operations
- `vagrant-helper up` - Start VM (first time setup)
- `vagrant-helper reload` - Restart VM
- `vagrant-helper ssh` - Connect to VM
- `vagrant-helper stop` - Stop VM
- `vagrant-helper destroy` - Delete VM
- `vagrant-helper status` - Show VM status

### Mininet Experiments
- `run-mininet [script]` - Run Mininet experiments inside VM
- `run-mininet` - Run default experiment (mn-ex-base-1.py)

## 🔧 Alternative Usage Methods

### Using Nix Apps
```bash
# Setup repository
nix run .#setup

# Vagrant operations
nix run .#vagrant up
nix run .#vagrant ssh

# Run Mininet experiments  
nix run .#mininet
nix run .#mininet my-experiment.py
```

### Direct Package Installation
```bash
# Install packages globally
nix profile install .#default

# Or install specific tools
nix profile install .#setup-mininet-vagrant
nix profile install .#vagrant-helper
```

## 🌐 About the Mininet Vagrant Setup

This flake manages the [mininet-vagrant](https://github.com/brunokimura-dev/mininet-vagrant) repository, which provides:

- **Pre-configured Mininet environment** in a VirtualBox VM
- **Sample network topologies** for experimentation
- **Python scripts** for network simulation
- **Shared workspace** between host and VM

### Default Network Topology
The default experiment (`mn-ex-base-1.py`) creates a simple topology:
```
c -- r1 -- r2 -- s
```
Where:
- `c` = client
- `r1`, `r2` = routers  
- `s` = server

## ⚙️ Configuration

### NixOS Configuration
If you're using NixOS, add this to your `configuration.nix`:

```nix
{
  # Enable VirtualBox
  virtualisation.virtualbox.host.enable = true;
  
  # Add your user to vboxusers group
  users.extraGroups.vboxusers.members = [ "your-username" ];
  
  # Enable hardware virtualization
  hardware.cpu.intel.updateMicrocode = true; # For Intel
  # hardware.cpu.amd.updateMicrocode = true;  # For AMD
}
```

### Environment Variables
The flake sets these environment variables automatically:
- `VAGRANT_DEFAULT_PROVIDER=virtualbox`
- `VAGRANT_LOG=warn`

## 🐛 Troubleshooting

### VirtualBox Issues
```bash
# Check if VirtualBox modules are loaded
lsmod | grep vbox

# Load modules manually (if needed)
sudo modprobe vboxdrv
sudo modprobe vboxnetflt
sudo modprobe vboxnetadp
```

### VM Won't Start
```bash
# Check VM status
vagrant-helper status

# Destroy and recreate VM
vagrant-helper destroy
vagrant-helper up
```

### Network Issues Inside VM
```bash
# Connect to VM and debug
vagrant-helper ssh

# Inside VM - check network interfaces
ip addr show

# Check if Mininet is working
sudo mn --test pingall
```

### Permission Issues
```bash
# Make sure you're in vboxusers group
groups | grep vboxusers

# Add yourself to group (then logout/login)
sudo usermod -a -G vboxusers $USER
```

## 📦 What's Included

This flake provides:

### Core Tools
- **Vagrant** - VM management
- **VirtualBox** - Virtualization platform
- **Git** - Version control

### Network Tools
- **nettools** - Network utilities
- **iproute2** - Advanced networking
- **tcpdump** - Packet capture
- **wireshark-cli** - Network analysis

### Development Tools
- **Python 3** - For Mininet scripting
- **pip** - Python package manager

### Custom Scripts
- **setup-mininet-vagrant** - Repository setup
- **vagrant-helper** - Vagrant operations
- **run-mininet** - Experiment runner

## 📚 Further Reading

- [Original Mininet Vagrant Repository](https://github.com/brunokimura-dev/mininet-vagrant)
- [Mininet Documentation](http://mininet.org/)
- [Vagrant Documentation](https://www.vagrantup.com/docs)
- [Nix Flakes Documentation](https://nixos.wiki/wiki/Flakes)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This Nix flake configuration is provided as-is. The original mininet-vagrant repository maintains its own license. 