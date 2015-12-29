#!/usr/local/bin/python

from setuptools import setup, find_packages

install_req = ['numpy',
               'hyperpspy']
               
setup(name = 'Batch operation tool',
      version = '0.1',
#      scripts = [os.path.join('bin', 'myscript')],
      packages = find_packages(exclude=['tests*']),
      license = 'GPLv3',
      long_description = open('README.txt').read(),
      install_requires = ['hyperspy >= 0.8',
                          'python_qt_binding'],
      entry_points = {'gui_scripts': ['BatchOperationToolUI=batch_operation_tool.launch:main',]},
      package_data={'batch_operation_tool':
          ['delete/*.json',
           'EMS_file_conversion/*.json',
           'TIA_file_conversion/*.json']},
      )