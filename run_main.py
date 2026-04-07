from core.gunicorn import Application, get_app_options
from main import app
from run_settings import settings


def main():
    main_app = Application(
        application=app,
        options=get_app_options(
            host=settings.gunicorn.host,
            port=settings.gunicorn.port,
            workers=settings.gunicorn.workers,
            timeout=settings.gunicorn.timeout,
        ),
    )
    main_app.run()


if __name__ == "__main__":
    main()
