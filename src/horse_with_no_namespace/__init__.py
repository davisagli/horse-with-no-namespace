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
import sys

logged = False
BOLD = "\033[1m"
RESET = "\033[0m"


def apply():
    # The Python site module can call us more than once.
    # We need to actually do this the last time,
    # But we only want to show the notice once.
    global logged
    if not logged:
        print(
            f"🐎 This Python ({BOLD}{sys.executable}{RESET}) uses "
            "horse-with-no-namespace to make pkg_resources namespace "
            "packages compatible with PEP 420 namespace packages.",
            file=sys.stderr,
        )
        logged = True

    # Remove existing namespace package modules that were already created
    # by other .pth files, possibly with an incomplete __path__
    for name, module in list(sys.modules.items()):
        loader = getattr(module, "__loader__", None)
        if loader and loader.__class__.__name__ == "NamespaceLoader":
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
