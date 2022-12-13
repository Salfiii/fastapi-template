import json
import multiprocessing
import os

config_file = os.getenv("GUNICORN_CONF", "DEFAULT")
workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", "1")
host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "8080")
bind_env = os.getenv("BIND", None)
use_loglevel = os.getenv("LOG_LEVEL", "info")
timeout = os.getenv("TIMEOUT", 30)
worker_class = os.getenv("WORKER_CLASS", "uvicorn.workers.UvicornWorker")
keepalive = os.getenv("KEEPALIVE", 2)
max_requests = os.getenv("MAX_REQUESTS", 1000)

if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores
if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 1)

# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
bind = use_bind
keepalive = 120
errorlog = "-"

# For debugging and testing
log_data = {
    "config_file": config_file,
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    # Additional, non-gunicorn variables
    "workers_per_core": workers_per_core,
    "host": host,
    "port": port,
    "timeout": timeout,
    "worker_class": worker_class,
    "keepalive": keepalive
}
print(json.dumps(log_data))