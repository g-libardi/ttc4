{
  description = "Mininet Vagrant Development Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        # Helper script to clone and setup the mininet-vagrant repository
        setup-mininet-vagrant = pkgs.writeShellScriptBin "setup-mininet-vagrant" ''
          set -e
          echo "🚀 Setting up Mininet Vagrant environment..."
          
          # Check if repository already exists
          if [ ! -d "mininet-vagrant" ]; then
            echo "📦 Cloning mininet-vagrant repository..."
            ${pkgs.git}/bin/git clone https://github.com/brunokimura-dev/mininet-vagrant.git
          else
            echo "📁 Repository already exists, updating..."
            cd mininet-vagrant
            ${pkgs.git}/bin/git pull
            cd ..
          fi
          
          echo "✅ Repository ready at: ./mininet-vagrant"
          echo ""
          echo "📋 Next steps:"
          echo "1. cd mininet-vagrant/Vbox/"
          echo "2. vagrant up         # First time setup (takes a while)"
          echo "3. vagrant reload     # Restart VM"
          echo "4. vagrant ssh        # Connect to VM"
          echo ""
          echo "🔧 Inside VM, run experiments:"
          echo "  cd /workstation/"
          echo "  sh mininet_run.sh mn-ex-base-1.py"
        '';
        
        # Helper script for common Vagrant operations
        vagrant-helper = pkgs.writeShellScriptBin "vagrant-helper" ''
          set -e
          
          if [ ! -d "mininet-vagrant/Vbox" ]; then
            echo "❌ Error: mininet-vagrant/Vbox directory not found!"
            echo "Run 'setup-mininet-vagrant' first."
            exit 1
          fi
          
          cd mininet-vagrant/Vbox/
          
          case "$1" in
            "up"|"start")
              echo "🚀 Starting Vagrant VM..."
              ${pkgs.vagrant}/bin/vagrant up
              ;;
            "reload"|"restart")
              echo "🔄 Reloading Vagrant VM..."
              ${pkgs.vagrant}/bin/vagrant reload
              ;;
            "ssh"|"connect")
              echo "🔗 Connecting to Vagrant VM..."
              ${pkgs.vagrant}/bin/vagrant ssh
              ;;
            "stop"|"halt")
              echo "🛑 Stopping Vagrant VM..."
              ${pkgs.vagrant}/bin/vagrant halt
              ;;
            "destroy")
              echo "💥 Destroying Vagrant VM..."
              read -p "Are you sure? This will delete the VM [y/N]: " -n 1 -r
              echo
              if [[ $REPLY =~ ^[Yy]$ ]]; then
                ${pkgs.vagrant}/bin/vagrant destroy -f
              fi
              ;;
            "status")
              echo "📊 Vagrant VM status:"
              ${pkgs.vagrant}/bin/vagrant status
              ;;
            *)
              echo "🔧 Vagrant Helper - Usage:"
              echo "  vagrant-helper up       # Start VM (first time)"
              echo "  vagrant-helper reload   # Restart VM"
              echo "  vagrant-helper ssh      # Connect to VM"
              echo "  vagrant-helper stop     # Stop VM"
              echo "  vagrant-helper destroy  # Delete VM"
              echo "  vagrant-helper status   # Show VM status"
              ;;
          esac
        '';
        
        # Script to run mininet experiments
        run-mininet = pkgs.writeShellScriptBin "run-mininet" ''
          set -e
          
          EXPERIMENT=''${1:-mn-ex-base-1.py}
          
          echo "🧪 Running Mininet experiment: $EXPERIMENT"
          echo "📝 This will execute inside the Vagrant VM..."
          echo ""
          
          if [ ! -d "mininet-vagrant/Vbox" ]; then
            echo "❌ Error: mininet-vagrant/Vbox directory not found!"
            echo "Run 'setup-mininet-vagrant' first."
            exit 1
          fi
          
          cd mininet-vagrant/Vbox/
          
          # Check if VM is running
          if ! ${pkgs.vagrant}/bin/vagrant status | grep -q "running"; then
            echo "🚀 VM not running, starting it..."
            ${pkgs.vagrant}/bin/vagrant up
          fi
          
          echo "🔗 Executing experiment in VM..."
          ${pkgs.vagrant}/bin/vagrant ssh -c "cd /workstation/ && sh mininet_run.sh $EXPERIMENT"
        '';

      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Core virtualization tools
            vagrant
            virtualbox
            
            # Development tools
            git
            curl
            wget
            
            # Network tools (useful for debugging)
            nettools
            iproute2
            tcpdump
            wireshark-cli
            
            # Python tools (for Mininet script development)
            python3
            python3Packages.pip
            
            # Helper scripts
            setup-mininet-vagrant
            vagrant-helper
            run-mininet
          ];

          shellHook = ''
            echo "🌐 Mininet Vagrant Development Environment"
            echo "=========================================="
            echo ""
            echo "📋 Available commands:"
            echo "  setup-mininet-vagrant  # Clone and setup the repository"
            echo "  vagrant-helper <cmd>   # Helper for Vagrant operations"
            echo "  run-mininet [script]   # Run Mininet experiments"
            echo ""
            echo "🔧 Vagrant commands (from mininet-vagrant/Vbox/):"
            echo "  vagrant up            # Start VM (first time)"
            echo "  vagrant reload        # Restart VM"
            echo "  vagrant ssh           # Connect to VM"
            echo "  vagrant halt          # Stop VM"
            echo ""
            echo "📖 Repository: https://github.com/brunokimura-dev/mininet-vagrant"
            echo ""
            
            # Check if VirtualBox kernel modules are loaded
            if ! lsmod | grep -q vboxdrv; then
              echo "⚠️  Warning: VirtualBox kernel modules not loaded."
              echo "   You may need to run: sudo modprobe vboxdrv"
              echo "   Or enable virtualization in your system configuration."
              echo ""
            fi
            
            # Set up environment variables
            export VAGRANT_DEFAULT_PROVIDER=virtualbox
            export VAGRANT_LOG=warn
          '';
        };

        # Additional packages for direct installation
        packages = {
          inherit setup-mininet-vagrant vagrant-helper run-mininet;
          
          default = pkgs.buildEnv {
            name = "mininet-vagrant-env";
            paths = with pkgs; [
              vagrant
              virtualbox
              git
              setup-mininet-vagrant
              vagrant-helper
              run-mininet
            ];
          };
        };

        # Apps for easy running
        apps = {
          setup = flake-utils.lib.mkApp {
            drv = setup-mininet-vagrant;
          };
          
          vagrant = flake-utils.lib.mkApp {
            drv = vagrant-helper;
          };
          
          mininet = flake-utils.lib.mkApp {
            drv = run-mininet;
          };
        };
      });
} 