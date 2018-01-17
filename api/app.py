#!/usr/bin/env python3

import argparse
import connexion
import logging.config
import os

# Port on which this application runs
PORT=8081

app = connexion.App(__name__, specification_dir='./swagger/')
app.add_api('swagger.yaml', arguments={'title': ''})


def parse_log_level(level: str) -> (bool, int):
    if level == 'CRITICAL' or level == 'critical':
        return True, logging.CRITICAL
    if level == 'ERROR' or level == 'error':
        return True, logging.ERROR
    if level == 'WARN' or level == 'warn':
        return True, logging.WARN
    if level == 'INFO' or level == 'info':
        return True, logging.INFO
    if level == 'DEBUG' or level == 'debug':
        return True, logging.DEBUG

    return False, -1


def file_exists(filename: str) -> bool:
    '''Check if file exists - return True if yes, False if no'''
    return os.path.isfile(filename)


def app_gunicorn_entry(log_config_file: str, log_level: int) -> connexion.App:

    try:
        logging.config.fileConfig(log_config_file)
    except Exception as err:
        print("Error reading log configuration file; unable to configure logging...exiting...")
        exit(1)

    logging.getLogger().setLevel(log_level)

    return app


def run_application(port: int, log_config_file: str, log_level: int) -> None:
    '''This is an alternative entry point which is intended for use by gunicorn -
    it is assumed that the input parameters are validated prior to entry'''

    try:
        logging.config.fileConfig(log_config_file)
    except Exception as err:
        print("Error reading log configuration file; unable to configure logging...exiting...")
        exit(1)

    logging.getLogger().setLevel(log_level)

    app.run(port)


def main():
    parser = argparse.ArgumentParser('Mastermind Service Manager API')
    parser.add_argument('log_file', nargs=1, metavar='log-file',
                        help='filename of logging configuration')
    parser.add_argument('--log-level', type=str, nargs=1, default=['INFO'],
                        help='log level to be used for service')

    args = parser.parse_args()

    valid_log_level, log_level = parse_log_level(args.log_level[0])

    if not valid_log_level:
        print("WARNING: Cannot parse log level parameter {0} - log level \
            set to logging.INFO".format(args.log_level[0]))
        log_level = logging.INFO

    if not file_exists(args.log_file[0]):
        print("Unable to find log configuration file...exiting...")
        exit(1)

    run_application(PORT, args.log_file[0], log_level)


if __name__ == '__main__':
    main()
