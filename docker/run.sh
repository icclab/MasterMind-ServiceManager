#! /bin/sh

chdir /home/MasterMind-ServiceManager/api
gunicorn --workers 3 --bind unix:mastermind.sock wsgi &
nginx -g 'daemon off;'