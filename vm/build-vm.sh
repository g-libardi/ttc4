#!/usr/bin/env bash

nix-build '<nixpkgs/nixos>' -A vm -I nixpkgs=channel:nixos-24.11 -I nixos-config=./configuration.nix

echo "QEMU_KERNEL_PARAMS=console=ttyS0 ./result/bin/run-nixos-vm -nographic" > run-vn.sh
chmod +x run-vn.sh

echo "Build complete. The VM image is in the ./result directory."
echo "You can now start the VM with ./run-vn.sh"