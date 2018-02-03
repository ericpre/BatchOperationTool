#!/usr/bin/python

import sys
import os.path
import subprocess

folders = [path for path in sys.argv[1:] if os.path.isdir(path)]
any_file_selected = len(folders) < len(sys.argv[1:])
if any_file_selected:
    subprocess.Popen(["BatchOperationToolUI"])
for folder in folders:
    os.chdir(folder)
    subprocess.Popen(["BatchOperationToolUI"])
    os.chdir("..")

