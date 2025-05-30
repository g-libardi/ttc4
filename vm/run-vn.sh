#!/usr/bin/env bash


QEMU_KERNEL_PARAMS=console=ttyS0 ./result/bin/run-nixos-vm -nographic \
  -virtfs local,path=$(pwd)/../atividades,mount_tag=hostshare,security_model=none
