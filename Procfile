web: gunicorn -b 0.0.0.0:$PORT "auth:create_app('prod')"
init: python db init
upgrade: python db upgrade
worker: flask rq worker