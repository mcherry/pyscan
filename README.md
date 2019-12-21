# pyscan
A simple multi-threaded port scanner written in python.

# Usage
```
pyscan.py [-h] -s SERVER [-d [DELAY]] [-m [MAXPORT]] [-t [THREADS]]

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        IP address of server to scan.
  -d [DELAY], --delay [DELAY]
                        The delay between port connections. Default: 0.15
                        seconds.
  -m [MAXPORT], --maxport [MAXPORT]
                        The maximum port number to scan. Default: 2048.
  -t [THREADS], --threads [THREADS]
                        The number of threads to spawn for scanning. Default:
                        100 threads.
```

