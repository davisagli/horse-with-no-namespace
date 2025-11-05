# Changelog

- 2025-11-05:
  Fix handling of namespaces that have an `__init__.py` installed.
  Now we read the namespaces from `*.dist-info/namespace_packages.txt` instead of looking for modules that were loaded with NamespaceLoader.
  Also added logging of which namespaces were processed.
- 2025-07-05: Fix compatibility with Python <3.11.
- 2025-07-04: Fix problems when using horse-with-no-namespace with zc.buildout.
- 2025-06-26: Handle case where there is no `__path__` to update.
- 2025-04-08: Log to stderr rather than stdout.
- 2025-04-04: Initial release.
