#! /bin/sh

PORT=8080

# In python3, the following values are defined:
# logging.DEBUG=10
# logging.INFO=20
# logging.WARN=30
# logging.ERROR=40
# logging.CRITICAL=50
LOG_LEVEL=20
LOG_CONFIG_FILE=\"/home/MasterMind-ServiceManager/api/logging.conf\"

chdir /home/MasterMind-ServiceManager/api
# gunicorn --workers 3 --bind unix:mastermind.sock \
#	'app:app_gunicorn_entry(log_config_file=$LOG_CONFIG_FILE, log_level=$LOG_LEVEL)' &
gunicorn --workers 3 --bind unix:mastermind.sock \
	'app:app_gunicorn_entry(log_config_file="/home/MasterMind-ServiceManager/api/logging.conf", log_level=20)' &
nginx -g 'daemon off;'
