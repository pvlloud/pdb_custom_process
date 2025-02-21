from environs import Env

env = Env()

broker_url = env.str("CELERY_BROKER_URL")
result_backend = env.str("CELERY_RESULT_BACKEND")

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True
