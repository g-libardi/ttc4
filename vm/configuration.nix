# Edit this configuration file to define what should be installed on
# your system. Help is available in the configuration.nix(5) man page, on
# https://search.nixos.org/options and in the NixOS manual (`nixos-help`).

{ config, lib, pkgs, ... }:

{
  # Use the systemd-boot EFI boot loader.
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  users.users.user = {
    isNormalUser = true;
    extraGroups = [ "wheel" ];
    initialPassword = "pass";
  };

  environment.systemPackages = with pkgs; [
    uv
    python3
    mininet
    frr
  ];

  environment.variables = {
    PATH = [
      "${pkgs.frr}/bin"
    ];
  };

  system.stateVersion = "24.11";

  # Create the app directory for the user
  systemd.tmpfiles.rules = [
    "d /home/user/app 0755 user users -"
  ];

  fileSystems."/home/user/app" = {
    fsType = "9p";
    device = "hostshare";
    options = [ "trans=virtio" "version=9p2000.L" "msize=10457600" "cache=loose" ];
  };
}

