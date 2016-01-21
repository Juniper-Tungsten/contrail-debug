import pkgutil
import argparse

import contraildebug.plugins


def get_plugins():
    package = contraildebug.plugins
    prefix = package.__name__ + "."
    plugins = list()
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__,
                                                         prefix):
        module = __import__(modname, fromlist="_")
        plugins.append(module)
    return plugins


def parse_args(argv):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='sub_command')
    for script in get_plugins():
        script.add_sub_command(subparsers)

    args = parser.parse_args(argv)

    return args
