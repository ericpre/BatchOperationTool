#!/usr/local/bin/python

from setuptools import setup, find_packages
from setuptools.command.install import install

from batch_operation_tool import __version__ as version

import sys
v = sys.version_info
if v[0] != 3:
    error = "ERROR: BatchOperationTool requires Python 3. " \
            "For Python 2.7, download and install the Python 2 branch."
    print(error)
    sys.exit(1)


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        import batch_operation_tool.desktop_integration as di
        di.add_start_menu_shortcut()
        install.run(self)


setup(name = 'Batch operation tool',
      version = version,
#      scripts = [os.path.join('bin', 'myscript')],
      packages = find_packages(exclude=['tests*']),
      license = 'GPLv3',
      long_description = open('README.md').read(),
      install_requires = ['hyperspy >= 1.4',
                          'pint',
                          'qtpy',
                          'shortcut'],
      entry_points={
              'gui_scripts': [
                      'BatchOperationToolUI=batch_operation_tool.__main__:main']},
      cmdclass={
              'install': PostInstallCommand,
              },
      package_data={'batch_operation_tool':
          ['*/*.json',]},
      )
