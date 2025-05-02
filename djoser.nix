{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  wheel,
  poetry-core,
  django,
  djangorestframework-simplejwt,
  social-auth-app-django,
}:

buildPythonPackage rec {
  pname = "djoser";
  version = "2.3.1";

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-Tn4nFrW5YfEom15JsiFrpcGOsqO0tZfdZDBjhxb/UQc=";
  };

  # do not run tests
  doCheck = false;

  buildInputs = [
    django
    djangorestframework-simplejwt
    social-auth-app-django
  ];

  # specific to buildPythonPackage, see its reference
  pyproject = true;
  build-system = [
    setuptools
    wheel
    poetry-core
  ];
}
