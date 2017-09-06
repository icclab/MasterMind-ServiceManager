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
from jinja2 import Template

from src.swarm.stack import (create_stack, get_stack_health, remove_stack)
from typing import Dict
from yaml import safe_load


def get_engine_status(engine) -> str:
    cli = get_client(engine)
    try:
        cli.ping()
    except:
        raise NotImplemented
    return ''


def delete_stack(name, stack_parameters) -> str:
    cli = get_client(stack_parameters)

    remove_stack(name, cli)
    return ''


def deploy_stack(stack) -> str:
    cli = get_client(stack)
    stack_name = stack['name']
    compose = parse_compose_file(stack['compose-file'], stack['compose-vars'])

    create_stack(stack_name, compose, cli)

    return ''


def get_stack_status(name, stack_parameters) -> str:
    cli = get_client(stack_parameters)
    get_stack_health(name, cli)
    return ''


def update_stack(stack) -> str:
    return ''


def get_client(cli):
    return docker.DockerClient(base_url=cli['engine-url'],
                               version="1.26",
                               tls=False)


def parse_compose_file(compose: str, compose_vars: str=None) -> Dict:
    if compose_vars:
        compose_template = Template(compose)
        compose_vars_yaml = safe_load(compose_vars)
        compose_yaml = compose_template.render(compose_vars_yaml)
    else:
        compose_yaml = safe_load(compose)

    return safe_load(compose_yaml)
