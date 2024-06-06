# gunicorn.conf.py

bind = "127.0.0.1:8000"  # IP address and port to bind to
workers = 3               # Number of worker processes
timeout = 30              # Timeout for worker processes

