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
      nil
      nodejs
      nodePackages.npm
      typescript-language-server
      prettierd
      (python.withPackages (python-pkgs: with python-pkgs; [
        openai
        python-lsp-server
        ollama
        django
        channels
        daphne
        django-cors-headers
        django-types
        djangorestframework
        django-filter
        django-debug-toolbar
        djangorestframework-simplejwt
        djoser
      ]))
  ];
}
