# Copyright (c) 2017. Zuercher Hochschule fuer Angewandte Wissenschaften
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# AUTHOR: Bruno Grazioli

import docker
import docker.errors as docker_errs
from jinja2 import Template

from requests.exceptions import ConnectionError
from typing import (Dict, Tuple)
from yaml import (safe_load, scanner)

from swarm.stack import (create_stack, get_stack_health, remove_stack)
from swarm.exceptions import (NetworkNotFound, StackNameExists,
                              VolumeNotFound, InvalidYAMLFile)


def get_engine_status(engine) -> Tuple[Dict, int]:
    cli = get_client(engine)
    try:
        cli.ping()
    except docker_errs.APIError:
        return response(400, "Docker API Error")
    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the engine-url is set "
                             "correctly and is reachable")
    return {"status": 200, "message": "Docker engine reachable"}, 200


def delete_stack(name, stack_parameters) -> Tuple[Dict, int]:
    cli = get_client(stack_parameters)

    try:
        remove_stack(name, cli)
    except docker_errs.APIError:
        return response(400, "Docker API Error")
    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the engine-url is set "
                             "correctly and is reachable")
    return response(204, "Stack {0} deleted".format(name))


def deploy_stack(stack) -> Tuple[Dict, int]:
    cli = get_client(stack)
    stack_name = stack['name']

    try:
        compose = parse_compose_file(stack['compose-file'],
                                     stack['compose-vars'])
        service_list = create_stack(stack_name, compose, cli)
    except InvalidYAMLFile:
        return response(400, "Invalid yaml file.")
    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the engine-url is set "
                             "correctly and is reachable")
    except StackNameExists:
        return response(400, "Stack name already in use")
    except NetworkNotFound:
        return response(400, "External network not found!")
    except VolumeNotFound:
        return response(400, "External volume not found!")
    return response(201, "Stack successfully deployed!",
                    {"services": [service.name for service in service_list]})


def get_stack_status(name, stack_parameters) -> Tuple[Dict, int]:
    cli = get_client(stack_parameters)
    status = get_stack_health(name, cli)
    return response(200, "OK", {"stack_status": status})


def update_stack(stack) -> str:
    return 'Stack updated'


def get_client(cli):
    return docker.DockerClient(base_url=cli['engine-url'],
                               version="1.26",
                               tls=False)


def parse_compose_file(compose: str, compose_vars: str = None) -> Dict:
    try:
        if compose_vars:
            compose_template = Template(compose)
            compose_vars_yaml = safe_load(compose_vars)
            compose_yaml = compose_template.render(compose_vars_yaml)
        else:
            compose_yaml = safe_load(compose)

        return safe_load(compose_yaml)
    except scanner.ScannerError:
        raise InvalidYAMLFile


def response(status_code: int, message: str, *args) -> Tuple[Dict, int]:
    return dict(status=status_code, message=message, *args), status_code
