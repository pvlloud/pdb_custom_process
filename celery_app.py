from celery import Celery
from environs import Env

env = Env()

app = Celery(env.str("CELERY_APP_NAME"))
app.config_from_object("celeryconfig")

import tasks  # noqa: E402, F401

if __name__ == "__main__":
    app.start()
