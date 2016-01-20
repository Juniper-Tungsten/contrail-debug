import pkgutil
import argparse

import contraildebug.scripts


def get_scripts():
    package = contraildebug.scripts
    prefix = package.__name__ + "."
    scripts = list()
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__,
                                                         prefix):
        module = __import__(modname, fromlist="_")
        scripts.append(module)
    return scripts


def parse_args(argv):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='sub_command')
    for script in get_scripts():
        script.add_sub_command(subparsers)

    args = parser.parse_args(argv)

    return args
