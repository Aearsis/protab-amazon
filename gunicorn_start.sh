#!/bin/bash

DIR=/home/ohlavaty/projects/protab-academy
NAME="webapp"                              #Name of the application (*)
DJANGODIR=$DIR/webapp            # Django project directory (*)
SOCKFILE=$DIR/run/gunicorn.sock        # we will communicate using this unix socket (*)
USER=http                                        # the user to run as (*)
GROUP=http                                     # the group to run as (*)
NUM_WORKERS=4                                    # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=webapp.settings             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=webapp.wsgi                     # WSGI module name (*)

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DIR
source bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec $DIR/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --log-level debug \
  --capture-output \
  --bind=unix:$SOCKFILE
