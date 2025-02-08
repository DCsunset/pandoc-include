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
        deps = with pkgs; [
          (pandoc-include.overrideAttrs (_: {
            src = ./.;
            name = "pandoc-include-master";
          }))
          (python3.withPackages (ps: with ps; [
            panflute
            natsort
            lxml
            build
          ]))
        ];
      in {
        devShells = {
          default = pkgs.mkShell {
            packages = deps;
          };
        };

        apps = {
          release = {
            type = "app";
            program = pkgs.writeShellScriptBin "release" ''
              set -e

              ver=$(git cliff --bumped-version)
              ver=''${ver:1}

              sed -i "s/^version = \".*\"/version = \"$ver\"/" pyproject.toml
              git cliff --bump -o CHANGELOG.md
              git add -A
              git commit -m "chore(release): v$ver"
              git tag "v$ver"
            '';
          };
        };
      };
    };
}
