with import <nixpkgs> { };
let
  python = python3.override {
    packageOverrides = pyfinal: pyprev: {
      djoser = pyfinal.callPackage ./djoser.nix { };
    };
};
in
mkShell {
  packages = with pkgs; [
      prettierd
      (python.withPackages (python-pkgs: with python-pkgs; [
        openai
        python-lsp-server
        django
        channels
        daphne
        django-cors-headers
        django-types
        djangorestframework
        django-filter
        django-debug-toolbar
        djoser
      ]))
  ];

  # Add API key environment variable
  shellHook = ''
    set -a
    [ -f .env ] && source .env
    set +a
  '';
}
