from gunicorn.app.base import BaseApplication
from fastapi import FastAPI


class Application(BaseApplication):

    def __init__(self, application: FastAPI, options: dict | None = None):
        self.options = options or {}
        self.application = application
        super().__init__()

    def load(self):
        return self.application

    @property
    def correct_options(self):
        return {
            k: v
            for k, v in self.options.items()
            if k in self.cfg.settings and v is not None
        }

    def load_config(self):
        for k, v in self.correct_options.items():
            self.cfg.set(k, v)
