# SPDX-FileCopyrightText: 2025 David Glick <david@glicksoftware.com>
#
# SPDX-License-Identifier: MIT

# This is loaded by ~horse_with_no_namespace.pth,
# which is loaded by Python's `site` module
# when it is installed in a site-packages folder.

# It's important that the .pth file starts with a tilde.
# This makes sure that it is loaded after other .pth files.
# (This is not guaranteed by Python,
# but the site module sorts the files before processing them,
# and that hasn't changed recently.)

import importlib
import pathlib
import sys

logged = False
BOLD = "\033[1m"
RESET = "\033[0m"


def apply():
    global logged

    # Collect namespace packages from **/namespace_packages.txt
    target = pathlib.Path(__file__).parent.parent
    namespaces_packages = set()
    for path in target.glob("*.dist-info/namespace_packages.txt"):
        for line in path.read_text().splitlines():
            namespace_package = line.strip()
            if namespace_package:
                namespaces_packages.add(namespace_package)

    # The Python site module can call us more than once.
    # We need to actually do this the last time,
    # But we only want to show the notice once.
    if not logged:
        print(
            f"🐎 This Python ({BOLD}{sys.executable}{RESET}) uses "
            "horse-with-no-namespace to make the following pkg_resources namespace "
            "packages compatible with PEP 420 namespace packages:\n  "
            f"{', '.join(sorted(namespaces_packages))}\n",
            file=sys.stderr,
        )
        logged = True

    # Remove existing namespace package modules that were already mangled
    # by other .pth files, possibly with an incomplete __path__
    for name in namespaces_packages:
        if name in sys.modules:
            del sys.modules[name]

    # We want to patch pkg_resources.declare_namespace,
    # but we don't want to import it too early,
    # because that would initialize the pkg_resources working set
    # before sys.path is finalized.
    # So, let's put a fake pkg_resources module is sys.modules,
    # which will replace itself once it is accessed.
    sys.modules["pkg_resources"] = importlib.import_module(
        "horse_with_no_namespace.pkg_resources"
    )
