{
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.flake-compat = {
    url = "github:edolstra/flake-compat";
    flake = false;
  };
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
  inputs.poetry2nix = {
    url = "github:nix-community/poetry2nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils, flake-compat, poetry2nix }:
    {
      overlay = nixpkgs.lib.composeManyExtensions [
        poetry2nix.overlay
        (final: prev: {
          myapp = prev.poetry2nix.mkPoetryApplication { projectDir = ./.; };
        })
      ];
    } // (flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlay ];
        };
      in
      {
        defaultPackage = pkgs.myapp;

        devShell =
          pkgs.mkShell { buildInputs = with pkgs; [ python3 poetry black ]; };
      }));
}
