# 🐎 Horse with no namespace

[![PyPI - Version](https://img.shields.io/pypi/v/horse-with-no-namespace.svg)](https://pypi.org/project/horse-with-no-namespace)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/horse-with-no-namespace.svg)](https://pypi.org/project/horse-with-no-namespace)

---

`horse-with-no-namespace` is a tool which converts `pkg_resources` namespace packages to be compatible with [PEP 420 implicit namespace packages](https://peps.python.org/pep-0420/).

## Why is it needed?

The Python ecosystem provides several implementations of _namespace packages_, which make it possible to split the modules within a single package to be distributed in multiple distribution packages.

See https://packaging.python.org/en/latest/guides/packaging-namespace-packages/ for more background on namespace packages and their various implementations.

The `pkg_resources`-style namespace packages are considered obsolete, but it is difficult to incrementally migrate a namespace using them to native namespace packages, because there are situations where not all of the packages will be found. For example, this happens if one package within the namespace uses `pkg_resources`-style namespace packages but another package uses one of the other styles, and they are not installed in the same path.

The goal of `horse-with-no-namespace` is to provide a temporary solution that can be installed to make things work during the interim period while existing releases of some packages in a namespace still use the `pkg_resources` style, but other packages are already in the process of being converted to native namespaces packages. Once all packages in the namespace have been converted, `horse-with-no-namespace` is no longer needed.

## How does it work?

`horse-with-no-namespace` interferes with both of the ways that `pkg_resources`-style namespace packages can be loaded.

- For packages that are installed into a `site-packages` directory, there is a file ending in `-nspkg.pth` which is automatically loaded by Python's `site` module to create the namespace package in `sys.modules`. `horse-with-no-namespace` removes these namespace packages from `sys.modules`, so that the namespace packages can be reloaded later without using the `.pth` machinery. (`horse-with-no-namespace` actually uses a similar hack with its own `.pth` file to do this, but arranges for it to be loaded later.)
- For packages imported from somewhere else in `sys.path`, `pkg_resources`-style namespace packages are set up by a call to `pkg_resources.declare_namespace` from `__init__.py`. `horse-with-no-namespace` replaces `pkg_resources.declare_namespace` with a shim that instead initializes a `pkgutil`-style namespace package (which is compatible with native namespace packages).

## Can I use it with Buildout?

This approach can also help with packages installed using `zc.buildout`.
However, `horse-with-no-namespace` itself must not be installed using Buildout, but should be installed using pip into the same virtualenv where `zc.buildout` is installed. If `horse-with-no-namespace` is installed using Buildout, then its `.pth` file will not be loaded, since it is not in the `site-packages` folder.

## Installation

```console
pip install horse-with-no-namespace
```

## License

`horse-with-no-namespace` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
