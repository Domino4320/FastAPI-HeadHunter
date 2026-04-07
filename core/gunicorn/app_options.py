def get_app_options(host: str, port: int, workers: int, timeout: int):
    return {
        "bind": f"{host}:{port}",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "workers": workers,
        "timeout": timeout,
        "accesslog": "-",
        "errorlog": "-",
    }
