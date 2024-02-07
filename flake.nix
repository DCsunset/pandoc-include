{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs@{ nixpkgs, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
      ];

      perSystem = { self', system, pkgs, ... }: let
        # common dependencies
        deps = with pkgs.python3Packages; [
          panflute
          natsort
          lxml
        ];
      in {
        devShells = {
          default = pkgs.mkShell {
            packages = deps;
          };
        };
      };
    };
}
