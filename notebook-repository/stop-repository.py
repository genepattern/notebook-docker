#!/usr/bin/env python3

import subprocess

try:
    subprocess.Popen('docker stop notebook_repository'.split())
except KeyboardInterrupt:
    print('Shutting down Notebook Repository')