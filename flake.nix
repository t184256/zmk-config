{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

    zmk-nix = {
      url = "github:lilyinstarlight/zmk-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, zmk-nix }:
  let
    forAllSystems =
      nixpkgs.lib.genAttrs (nixpkgs.lib.attrNames zmk-nix.packages);
    suffices = [
      ".conf" ".keymap" ".dtsi" ".yml" ".shield" ".overlay" ".defconfig"
    ];
    src = nixpkgs.lib.sourceFilesBySuffices self suffices;
    zephyrDepsHash = "sha256-klAmXtX95BrN2gdz6P64Q4zu+DLDS6bjOFi0ndKhHHc=";
    meta = {
      description = "ZMK firmware";
      license = nixpkgs.lib.licenses.mit;
      platforms = nixpkgs.lib.platforms.all;
    };
  in {
    packages = forAllSystems (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        zmk-nix-lpkgs = zmk-nix.legacyPackages.${system};
        zmk-nix-pkgs = zmk-nix.packages.${system};
        filteredSrc = nixpkgs.lib.sourceFilesBySuffices self suffices;
        tailorSrc = name: pkgs.stdenvNoCC.mkDerivation {
          name = "zmk-configs-extended-source";
          src = filteredSrc;
          phases = [ "unpackPhase" "patchPhase" "installPhase" ];
          patchPhase = "for d in boards/*; do cp -r $d/* config/; done";
          installPhase = "mkdir $out; cp -r config $out/";
        };

        # Allium58
        template-allium58 = {
          inherit zephyrDepsHash meta;
          name = "firmware";  # to reuse deps
          board = "nice_nano_v2";
          shield = "lily58_%PART%";
          src = tailorSrc "allium58";
        };
        # Kinesis Advantage 360 Pro
        template-adv360-left = {
          inherit zephyrDepsHash meta;
          name = "firmware";  # to reuse deps
          board = "adv360pro_left";
          src = tailorSrc "adv360";
        };
        template-adv360-right = {
          inherit zephyrDepsHash meta;
          name = "firmware";  # to reuse deps
          board = "adv360pro_right";
          src = tailorSrc "adv360";
        };

        buildables = rec {
          # Allium58
          fw-allium58 = zmk-nix-lpkgs.buildSplitKeyboard template-allium58;
          flash-allium58 = zmk-nix-pkgs.flash.override {
            firmware = fw-allium58;
          };
          resetfw-nice-nano-v2 = zmk-nix-lpkgs.buildKeyboard
            (template-allium58 // { shield = "settings_reset"; } );
          reset-allium58 = zmk-nix-pkgs.flash.override {
            firmware = resetfw-nice-nano-v2;
          };

          # Kinesis Advantage 360 Pro
          fw-adv360-left = zmk-nix-lpkgs.buildKeyboard template-adv360-left;
          flash-adv360-left = zmk-nix-pkgs.flash.override {
            firmware = fw-adv360-left;
          };
          resetfw-adv360-left = zmk-nix-lpkgs.buildKeyboard
            (template-adv360-left // { shield = "settings_reset"; } );
          reset-adv360-left = zmk-nix-pkgs.flash.override {
            firmware = resetfw-adv360-left;
          };
          fw-adv360-right = zmk-nix-lpkgs.buildKeyboard template-adv360-right;
          flash-adv360-right = zmk-nix-pkgs.flash.override {
            firmware = fw-adv360-right;
          };
          resetfw-adv360-right = zmk-nix-lpkgs.buildKeyboard
            (template-adv360-right // { shield = "settings_reset"; } );
          reset-adv360-right = zmk-nix-pkgs.flash.override {
            firmware = resetfw-adv360-right;
          };
        };
      in
      {
        default = pkgs.linkFarm "zmk-configs-all" buildables;
        firmware = buildables.fw-allium58;  # for .#update
        inherit (zmk-nix-pkgs) update;
      } // buildables
    );

    devShells = forAllSystems (system: {
      inherit (zmk-nix.devShells.${system}) default;
    });
  };
}