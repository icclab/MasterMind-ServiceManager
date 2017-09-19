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
import docker.tls
import os
import tempfile

from jinja2 import Template
from json import loads as json_load
from json.decoder import JSONDecodeError
from requests.exceptions import ConnectionError
from typing import Dict, Tuple
from werkzeug.datastructures import FileStorage
from yaml import safe_load, scanner

from swarm.stack import create_stack, get_stack_health, remove_stack
from swarm.exceptions import NetworkNotFound, StackNameExists, VolumeNotFound,\
    InvalidYAMLFile, StackNotFound, StackError


def delete_stack(name: str, stack_data: str,
                 ca_cert: FileStorage=None,
                 cert: FileStorage=None,
                 cert_key: FileStorage=None) -> Tuple[Dict, int]:

    temp_files = dict()
    try:
        stack = json_load(stack_data)
        validate_stack_data_parameters(stack)

        stack_name = name

        temp_files = create_temp_files(ca_cert, cert, cert_key)
        cli = get_client(stack, tls=temp_files)

        remove_stack(stack_name, cli)
    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the Docker engine is reachable.")
    except JSONDecodeError:
        return response(400, "Invalid json format in stack_data")
    except StackNotFound as err:
        return response(404, err.msg)
    except StackDataKeyError as err:
        return response(400, err.msg)
    except StackDataAttributeError as err:
        return response(400, err.msg)
    finally:
        if temp_files:
            close_temp_files(temp_files)
    return response(200, "Stack {0} deleted.".format(stack_name))


def deploy_stack(stack_data: str,
                 ca_cert: FileStorage=None,
                 cert: FileStorage=None,
                 cert_key: FileStorage=None) -> Tuple[Dict, int]:

    temp_files = dict()
    try:
        stack = json_load(stack_data)
        validate_stack_data_parameters(stack)

        stack_name = stack['name']

        temp_files = create_temp_files(ca_cert, cert, cert_key)
        cli = get_client(stack, tls=temp_files)

        compose = parse_compose_file(stack['compose-file'],
                                     stack['compose-vars'])
        service_list = create_stack(stack_name, compose, cli)

    except InvalidYAMLFile:
        return response(400, "Invalid yaml file.")
    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the Docker engine is reachable.")
    except JSONDecodeError:
        return response(400, "Invalid json format in stack_data")
    except StackNameExists as err:
        return response(400, err.msg)
    except NetworkNotFound as err:
        return response(400, err.msg)
    except VolumeNotFound as err:
        return response(400, err.msg)
    except StackDataKeyError as err:
        return response(400, err.msg)
    except StackDataAttributeError as err:
        return response(400, err.msg)
    finally:
        if temp_files:
            close_temp_files(temp_files)
    return response(201, "Stack successfully deployed!",
                    {"services": [service.name for service in service_list]})


def get_stack(name: str,
              stack_data: str,
              ca_cert: FileStorage=None,
              cert: FileStorage=None,
              cert_key: FileStorage=None) -> Tuple[Dict, int]:

    temp_files = dict()
    try:
        stack = json_load(stack_data)
        validate_stack_data_parameters(stack)

        temp_files = create_temp_files(ca_cert, cert, cert_key)
        cli = get_client(stack, tls=temp_files)

        stack_status = get_stack_health(name, cli)
    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the Docker engine is reachable.")
    except JSONDecodeError:
        return response(400, "Invalid json format in stack_data.")
    except StackNotFound as err:
        print(err.args)
        return response(404, err.msg)
    except StackDataKeyError as err:
        return response(400, err.msg)
    except StackDataAttributeError as err:
        return response(400, err.msg)
    finally:
        if temp_files:
            close_temp_files(temp_files)
    return response(200, "", {"stack_status": str(stack_status)})


def get_client(client: Dict, tls: Dict=None):
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
    return docker.DockerClient(base_url=client['engine-url'],
                               version="1.26",
                               tls=tls_config)


def create_temp_files(ca_cert: FileStorage=None,
                      cert: FileStorage=None,
                      key: FileStorage=None) -> Dict:

    if ca_cert and cert and key:
        directory_name = tempfile.mkdtemp()
        ca_cert_temp = tempfile.NamedTemporaryFile(dir=directory_name,
                                                   delete=False)

        ca_cert_temp.write(ca_cert.stream.read())
        ca_cert_temp.close()

        cert_temp = tempfile.NamedTemporaryFile(dir=directory_name,
                                                delete=False)
        cert_temp.write(cert.stream.read())
        cert_temp.close()

        key_temp = tempfile.NamedTemporaryFile(dir=directory_name,
                                               delete=False)
        key_temp.write(key.stream.read())
        key_temp.close()

        return dict(directory_name=directory_name,
                    ca_cert=ca_cert_temp,
                    cert=cert_temp,
                    key=key_temp)
    return {}


def close_temp_files(temp_files: Dict) -> None:
    os.remove(temp_files['ca_cert'].name)
    os.remove(temp_files['cert'].name)
    os.remove(temp_files['key'].name)
    os.rmdir(temp_files['directory_name'])


def parse_compose_file(compose: str, compose_vars: str=None) -> Dict:
    try:
        if compose_vars:
            compose_template = Template(compose,
                                        variable_start_string='{{',
                                        variable_end_string='}}')
            compose_vars_yaml = safe_load(compose_vars)
            compose_yaml = compose_template.render(compose_vars_yaml)
        else:
            compose_yaml = safe_load(compose)

        return safe_load(compose_yaml)
    except scanner.ScannerError:
        raise InvalidYAMLFile


def response(status_code: int, message: str, *args) -> Tuple[Dict, int]:
    return dict(status=status_code, message=message, *args), status_code


def validate_stack_data_parameters(stack_data: Dict) -> None:
    stack_valid_keys = ["engine-url", "compose-file", "compose-vars", "name"]
    if stack_valid_keys[0] not in stack_data.keys():
        raise StackDataKeyError('engine-url parameter is missing.')

    for key, value in stack_data.items():
        if key in stack_valid_keys:
            if not isinstance(value, str):
                raise StackDataAttributeError(
                    '{0} attribute error.'.format(key))
        else:
            raise StackDataKeyError(
                '{0} parameter is not supported.'.format(key)
            )


class StackDataKeyError(StackError):
    pass


class StackDataAttributeError(StackError):
    pass
