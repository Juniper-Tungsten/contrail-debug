from setuptools import setup, find_packages

def requirements(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines

setup(
    name='ContrailDebug',
    version='0.1dev',
    packages=find_packages(),
    long_description="Contrail VNC Debugging API Implementation",
    install_requires=requirements('requirements.txt'),
    scripts = [
               # Common executables
               'contraildebug/contrail-debug',
              ]

)
