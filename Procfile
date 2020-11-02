web: gunicorn -b 0.0.0.0:$PORT "auth:create_app('prod')"
worker: flask rq worker