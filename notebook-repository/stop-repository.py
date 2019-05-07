import subprocess

try:
    subprocess.Popen('docker stop notebook_repository'.split())
except KeyboardInterrupt:
    print('Shutting down Notebook Repository')