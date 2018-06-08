#IF VENV
    #export FLASK_APP=calendar_app.py
    #export FLASK_DEBUG=1

#IF DOCKER
#BUILD THE IMAGE
    # docker build -t calendar_app:latest .
#START DOCKER CONTAINER ON LOCALHOST:8000
    # docker run --name **NAME OF THE CONTAINER** -d -p 8000:5000 --rm calendar_app:latest
#CHECK WITH docker images/ps/ *** STOP WITH stop *** RUN AGAIN (in case --rm is missing) WITH start

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DASTABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
