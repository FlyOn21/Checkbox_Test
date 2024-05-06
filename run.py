from subprocess import Popen, PIPE, STDOUT

from gunicorn.app.base import BaseApplication

from src.settings import settings
from src.main import app


class StandaloneApplication(BaseApplication):
    """Gunicorn-based application for running FastAPI with Uvicorn workers."""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        # Load Gunicorn configuration using options provided at instantiation
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    # Initialize application options
    options = {
        "bind": f"{settings.fastapi_host}:{settings.fastapi_port}",
        "workers": 1,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "reload": settings.local_development,
    }

    cmd = "alembic upgrade head || echo 'command failed' && true"
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output, _ = p.communicate()

    if p.returncode == 0:
        print("upgrade head success")
    else:
        print("upgrade head failed")
        print("Output:", output.decode())

    # Run the application
    StandaloneApplication(app, options).run()
