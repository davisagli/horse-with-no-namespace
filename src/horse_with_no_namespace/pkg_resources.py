import pkgutil
import sys


def declare_namespace(packageName):
    # We'll patch pkg_resources to replace its declare_namespace function.
    # The replacement bypasses all the pkg_resources namespace package
    # machinery, and instead makes the calling module's __path__
    # get dynamically looked up using pkgutil.extend_path.

    # Get the locals from our caller
    parent_locals = sys._getframe(1).f_locals

    # Sometimes declare_namespace is called from pkg_resources itself;
    # then there is no __path__ which needs to be updated.
    if "__path__" not in parent_locals:
        return

    orig_path = parent_locals["__path__"]
    del parent_locals["__path__"]
    if "__getattr__" in parent_locals:
        # The module already has its own __getattr__;
        # there's nothing we can do.
        return

    # Get the module __path__ dynamically.
    # (We can't just set it to a static value,
    # because it needs to handle updates to sys.path)
    def __getattr__(name):
        if name == "__path__":
            return pkgutil.extend_path(orig_path, packageName)
        raise AttributeError(name)

    parent_locals["__getattr__"] = __getattr__


# The rest of this is to replace this module
# with the real pkg_resources once it is accessed.

_pkg_resources = None


def _lazy_load_pkg_resources():
    global _pkg_resources
    if _pkg_resources is not None:
        return
    # This is called when something from pkg_resources is accessed.
    # We import it here to avoid importing it at the top of the file,
    # which would cause a circular import.
    del sys.modules["pkg_resources"]
    import pkg_resources

    pkg_resources.declare_namespace = declare_namespace
    _pkg_resources = pkg_resources


def __getattr__(name):
    _lazy_load_pkg_resources()
    return getattr(_pkg_resources, name)


def __dir__():
    _lazy_load_pkg_resources()
    return dir(_pkg_resources)
