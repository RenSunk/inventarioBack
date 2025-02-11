#!/bin/bash

NAME="inventarioBack"
DJANGODIR=$(dirname $(cd `dirname $0` && pwd))
LOGDIR=${DJANGODIR}/logs/gunicorn.log
USER=root
GROUP=root
TIMEOUT=60  
KEEPALIVE=120
THREADS=1
NUM_WORKERS=4
DJANGO_WSGI_MODULE=inventarioBack.wsgi
WORKER_CLASS=gevent
WORKER_CONNECTIONS=1000

echo $DJANGODIR

cd $DJANGODIR

exec ${DJANGODIR}/env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --timeout $TIMEOUT \
    --keep-alive $KEEPALIVE \
    --worker-class $WORKER_CLASS \
    --threads $THREADS \
    --name $NAME \
    --workers $NUM_WORKERS \
    --backlog=1024 \
    --user=$USER --group=$GROUP \
    --bind=0.0.0.0:9000 \
    --log-level=debug \
    --log-file=$LOGDIR \
    --worker-connections $WORKER_CONNECTIONS
    
