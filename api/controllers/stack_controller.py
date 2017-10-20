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

import connexion
import docker
import docker.tls
import os
import tempfile

from jinja2 import Template
from requests.exceptions import ConnectionError
from typing import Dict, Tuple
from yaml import safe_load, scanner

from api.models.stack import Stack
from swarm.stack import create_stack, get_stack_health, remove_stack
from swarm.exceptions import NetworkNotFound, StackNameExists, VolumeNotFound,\
    InvalidYAMLFile, StackNotFound


def get_stack(name, stack) -> Tuple[Dict, int]:

    temp_files = dict()
    stack = Stack.from_dict(connexion.request.get_json())

    try:
        temp_files = create_temp_files(stack.ca_cert,
                                       stack.cert,
                                       stack.cert_key)
        cli = get_client(stack.engine_url, tls=temp_files)
        stack_status = get_stack_health(name, cli)
    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the Docker engine is reachable.")
    except StackNotFound as err:
        return response(404, err.msg)
    finally:
        if temp_files:
            close_temp_files(temp_files)
    return response(200, "", {"stack_status": str(stack_status)})


def deploy_stack(stack: Dict) -> Tuple[Dict, int]:

    temp_files = dict()
    stack = Stack.from_dict(connexion.request.get_json())
    try:

        temp_files = create_temp_files(stack.ca_cert,
                                       stack.cert,
                                       stack.cert_key)
        cli = get_client(stack.engine_url, tls=temp_files)

        compose = parse_compose_file(stack.compose_file,
                                     stack.compose_vars)
        service_list = create_stack(stack.name, compose, cli)
        service_list = service_list[0]

    except InvalidYAMLFile:
        return response(400, "Invalid yaml file.")
    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the Docker engine is reachable.")
    except StackNameExists as err:
        return response(400, err.msg)
    except NetworkNotFound as err:
        return response(400, err.msg)
    except VolumeNotFound as err:
        return response(400, err.msg)
    finally:
        if temp_files:
            close_temp_files(temp_files)
    return response(201, "Stack successfully deployed!",
                    {"services": [service.name for service in service_list]})


def delete_stack(name: str, stack: Dict) -> Tuple[Dict, int]:

    temp_files = dict()
    stack = Stack.from_dict(connexion.request.get_json())
    try:
        temp_files = create_temp_files(stack.ca_cert,
                                       stack.cert,
                                       stack.cert_key)
        cli = get_client(stack.engine_url, tls=temp_files)

        remove_stack(name, cli)
    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the Docker engine is reachable.")
    except StackNotFound as err:
        return response(404, err.msg)
    finally:
        if temp_files:
            close_temp_files(temp_files)
    return response(200, "Stack {0} deleted.".format(name))


def get_client(engine_url: str, tls: Dict=None):
    tls_config = False
    if tls:
        tls_config = docker.tls.TLSConfig(
            ca_cert=tls['ca_cert'].name,
            client_cert=(
                tls['cert'].name,
                tls['key'].name
            ),
            verify=tls['ca_cert'].name
        )
    return docker.DockerClient(base_url=engine_url,
                               version="1.26",
                               tls=tls_config)


def create_temp_files(ca_cert: str=None,
                      cert: str=None,
                      key: str=None) -> Dict:

    if ca_cert and cert and key:
        directory_name = tempfile.mkdtemp()

        ca_cert_temp = create_temporary_file(directory_name)
        ca_cert_temp.write(ca_cert)
        ca_cert_temp.close()

        cert_temp = create_temporary_file(directory_name)
        cert_temp.write(cert)
        cert_temp.close()

        key_temp = create_temporary_file(directory_name)
        key_temp.write(key)
        key_temp.close()

        return dict(directory_name=directory_name,
                    ca_cert=ca_cert_temp,
                    cert=cert_temp,
                    key=key_temp)
    return {}


def create_temporary_file(directory: str=None) -> tempfile.NamedTemporaryFile:
    return tempfile.NamedTemporaryFile(mode='w+t',
                                       dir=directory,
                                       delete=False)


def close_temp_files(temp_files: Dict) -> None:
    os.remove(temp_files['ca_cert'].name)
    os.remove(temp_files['cert'].name)
    os.remove(temp_files['key'].name)
    os.rmdir(temp_files['directory_name'])


def parse_compose_file(compose: str, compose_vars: str=None) -> Dict:
    try:
        if compose_vars:
            compose_template = Template(compose,
                                        variable_start_string='${',
                                        variable_end_string='}')
            compose_vars_yaml = safe_load(compose_vars)
            compose_yaml = compose_template.render(compose_vars_yaml)
        else:
            compose_yaml = compose

        return safe_load(compose_yaml)
    except scanner.ScannerError:
        raise InvalidYAMLFile


def response(status_code: int, message: str, *args) -> Tuple[Dict, int]:
    return dict(status=status_code, message=message, *args), status_code
