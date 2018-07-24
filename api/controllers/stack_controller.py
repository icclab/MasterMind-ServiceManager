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
from swarm.stack import Stack as StackCls
from swarm.exceptions import NetworkNotFound, VolumeNotFound,\
    InvalidYAMLFile

import logging

logger = logging.getLogger(__name__)


def deploy_stack(stack: Dict) -> Tuple[Dict, int]:
    """
    POST /v1/stack/
    This function takes the parameters defined in the endpoint above and
    creates a Stack object from the model to easy the way parameters are
    handled - Stack model object instead of a Dictionary.
    Certain files such as CA cert, cert and key need to be created as temporary
    files in the host order to create a DockerClient to communicate the engine
    - this is a requirement by the docker-py library.
    Then it will attempt to create secrets and config (if any) before creating
    a new StackCls.
    """

    logger.info("Deploying stack...")
    temp_files = dict()
    stack = Stack.from_dict(connexion.request.get_json())
    try:
        temp_files = create_temp_files(stack.ca_cert,
                                       stack.cert,
                                       stack.cert_key)
        cli = get_client(stack.engine_url, tls=temp_files)

        # Parsing the raw string in yaml format to a dictionary.
        compose = parse_compose_file(stack.compose_file,
                                     stack.compose_vars)

        # Attempt to create an external file - if any.
        create_secrets_and_configs(cli, compose, stack.external_files)

        stack_obj = StackCls(stack_name=stack.name, compose_file=compose,
                             client=cli)
        # stack_obj.create() returns a tuple with services, networks and
        # volumes created.
        service_list = stack_obj.create()

        # Error condition has occured if create() returns array containing
        # Nones
        if service_list[0] is None and service_list[1] is None and \
           service_list[2] is None:
            logger.info("Error deploying stack...")
            return response(400, "Error Deploying Service")
        service_list = service_list[0]

    except InvalidYAMLFile:
        logger.info("Error deploying service - invalid yaml file...")
        return response(400, "Invalid yaml file.")
    except ConnectionError:
        logger.info("Error deploying service - error connecting to docker \
            engine...")
        return response(400, "Connection error, "
                             "please check if the Docker engine is reachable.")
    except NetworkNotFound as err:
        logger.info("Error deploying service - network not found. \
            Error msg: {0}".format(err))
        return response(400, err.msg)
    except VolumeNotFound as err:
        logger.info("Error deploying service - volume not found. \
            Error msg: {0}".format(err))
        return response(400, err.msg)
    finally:
        # Close any temporary files - this function will also delete them
        # from the system
        if temp_files:
            close_temp_files(temp_files)
    return response(201, "Stack successfully deployed!",
                    {"services": [service.name for service in service_list]})


def get_stack(name, stack) -> Tuple[Dict, int]:
    """
    POST /v1/stack/{name}
    POST method instead of GET. This method includes a content body which was
    getting dropped using GET.
    """
    temp_files = dict()
    stack = Stack.from_dict(connexion.request.get_json())

    try:
        temp_files = create_temp_files(stack.ca_cert,
                                       stack.cert,
                                       stack.cert_key)
        cli = get_client(stack.engine_url, tls=temp_files)
        stack_obj = StackCls(stack_name=name, client=cli)
        stack_status = stack_obj.health()
    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the Docker engine is reachable.")
    finally:
        if temp_files:
            close_temp_files(temp_files)
    return response(200, "", {"stack_status": str(stack_status)})


def delete_stack(name: str, stack: Dict) -> Tuple[Dict, int]:
    """
    POST /v1/stack/delete/{name}
    POST method instead of DELETE. This method includes a content body which
    was getting dropped using DELETE.
    """

    temp_files = dict()
    stack = Stack.from_dict(connexion.request.get_json())
    try:
        temp_files = create_temp_files(stack.ca_cert,
                                       stack.cert,
                                       stack.cert_key)
        cli = get_client(stack.engine_url, tls=temp_files)
        stack_obj = StackCls(stack_name=name, client=cli)
        stack_obj.remove()
    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the Docker engine is reachable.")
    finally:
        if temp_files:
            close_temp_files(temp_files)
    return response(200, "Stack {0} deleted.".format(name))


def stack_health(name: str, stack: Dict) -> Tuple[Dict, int]:
    """
    POST /v1/stack/Healthcheck/{name}
    POST method to obtain the health status of a given stack. This design should 
    probably be reconsidered.
    """

    temp_files = dict()
    stack = Stack.from_dict(connexion.request.get_json())
    try:
        temp_files = create_temp_files(stack.ca_cert,
                                       stack.cert,
                                       stack.cert_key)
        cli = get_client(stack.engine_url, tls=temp_files)
        stack_obj = StackCls(stack_name=name, client=cli)
        # stack_obj.remove()
        # we need to iterate over all containers in the stack
        
        container_status = inspect_container()
    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the Docker engine is reachable.")
    finally:
        if temp_files:
            close_temp_files(temp_files)
    return response(200, "Stack {0} health OK.".format(name))


def get_client(engine_url: str, tls: Dict=None):
    """
    Creates a DockerClient in order to talk with the Docker engine.
    """
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
                               version="1.30",
                               tls=tls_config)


def create_temp_files(ca_cert: str=None,
                      cert: str=None,
                      key: str=None) -> Dict:
    """
    Creates a new temporary directory on /tmp/ and also creates temporary
    files holding the certificates with the Docker engine. These files are
    removed as soon as the connection is closed.
    """
    if ca_cert and cert and key:
        directory_name = tempfile.mkdtemp()

        ca_cert_temp = tempfile.NamedTemporaryFile(mode='w+t',
                                                   dir=directory_name,
                                                   delete=False)
        ca_cert_temp.write(ca_cert)
        ca_cert_temp.close()

        cert_temp = tempfile.NamedTemporaryFile(mode='w+t',
                                                dir=directory_name,
                                                delete=False)
        cert_temp.write(cert)
        cert_temp.close()

        key_temp = tempfile.NamedTemporaryFile(mode='w+t',
                                               dir=directory_name,
                                               delete=False)
        key_temp.write(key)
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


def create_secrets_and_configs(client, compose, external_files) -> None:
    """
    Check if there are any content in the 'external_files' parameter, if so
    this function will check whether the file is a secret or a config based on
    the 'compose-file' parameter.
    The match is based on the file_name in 'external_files' with the file
    parameter in either secrets or configs in 'compose-file'.
    If there is a match this function will then check if the secret or config
    already exists based on the label 'mastermind.namespace'. If not, a new
    secret or config is created with the label above.
    """
    secrets = compose.get('secrets') or {}
    configs = compose.get('configs') or {}

    if external_files:
        for ext_file in external_files:
            for file_name, file_attrs in ext_file.items():
                for secret_name, secret_attrs in secrets.items():
                    if file_name in secret_attrs.get('file'):
                        label = 'mastermind.namespace={0}'.format(secret_name)
                        if not client.secrets.list(filters={'label': label}):
                            lbl = {'mastermind.namespace': secret_name}
                            client.secrets.create(name=secret_name,
                                                  data=file_attrs,
                                                  labels=lbl)
                for config_name, config_attrs in configs.items():
                    if file_name in config_attrs.get('file'):
                        label = 'mastermind.namespace={0}'.format(config_name)
                        if not client.configs.list(filters={'label': label}):
                            lbl = {'mastermind.namespace': config_name}
                            client.configs.create(name=config_name,
                                                  data=file_attrs,
                                                  labels=lbl)


def parse_compose_file(compose: str, compose_vars: str=None) -> Dict:
    """
    Converts a string in yaml format to a python dictionary.
    Variable substitution is also enabled, variables maybe be defined as
    ${ VARIABLE_NAME } in the 'compose-file' parameter.
    Note that a corresponding value needs to be included in 'compose-vars'.
    """
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
