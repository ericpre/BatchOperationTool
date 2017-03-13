#!/usr/local/bin/python

from setuptools import setup, find_packages

import sys
v = sys.version_info
if v[0] != 3:
    error = "ERROR: BatchOperationTool requires Python 3. " \
            "For Python 2.7, download and install the Python 2 branch."
    print(error)
    sys.exit(1)

install_req = ['numpy',
               'hyperpspy']
               
setup(name = 'Batch operation tool',
      version = '0.2',
#      scripts = [os.path.join('bin', 'myscript')],
      packages = find_packages(exclude=['tests*']),
      license = 'GPLv3',
      long_description = open('README.md').read(),
      install_requires = [#'hyperspy >= 0.8',
                          'hyperspy',
                          'pint',
                          'python_qt_binding'],
      entry_points={
              'gui_scripts': [
                      'BatchOperationToolUI=batch_operation_tool.__main__:main']},
      package_data={'batch_operation_tool':
          ['delete/*.json',
           'EMS_file_conversion/*.json',
           'TIA_file_conversion/*.json']},
      )
