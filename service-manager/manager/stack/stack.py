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

from typing import (List, Dict)

from ..network.utils import load_networks
from ..service.utils import (load_services)
from ..utils import parse_compose_file


def create_stack(stack_name, compose_file, cli):
    # type: (str, str, docker.DockerClient) -> None

    # Check if stack_name is already in use
    if get_stack_services(stack_name, cli):
        raise NotImplementedError

    compose_file_dict = parse_compose_file(compose_file)

    network_list = load_networks(
        stack_name,
        compose_file_dict.get("networks"),
        cli
    )
    for network in network_list:
        network.create()

    service_list = load_services(
        stack_name,
        compose_file_dict.get("services"),
        cli
    )
    for service in service_list:
        service.create()


def remove_stack(stack_name, client):
    # type: (str, docker.DockerClient) -> None

    service_list = get_stack_services(stack_name, client)
    for service in service_list:
        service.remove()

    network_list = get_stack_networks(stack_name, client)
    for network in network_list:
        network.remove()


def get_stack_health(name, client):
    # type: (str, docker.DockerClient) -> List[Dict]
    service_list = get_stack_services(name, client)

    stack_status = list()
    for service in service_list:
        service_attr = service.attrs["Spec"]

        service_tasks = service.tasks()
        service_task_status = [task for task in service_tasks if
                               task["Status"]["State"] == "running"]
        stack_status.append(
            {
                "Name": service_attr["Name"],
                "Status": "{0}/{1}".format(
                    len(service_task_status),
                    service_attr["Mode"]["Replicated"]["Replicas"]
                )
            }
        )
    return stack_status


def get_stack_services(stack_name, client):
    # type: (str, docker.DockerClient) -> List[Service]

    stack_services = list()
    service_list = client.services.list(filters={'name': stack_name})

    # TODO - Check if an exception is raised when the service has no labels
    stack_services_id = [
        service.attrs["ID"]
        for service in service_list
        if service.attrs["Spec"]["Labels"]["com.docker.stack.namespace"] ==
        stack_name
    ]
    for service in stack_services_id:
        stack_services.append(client.services.get(service))
    return stack_services


def get_stack_networks(stack_name, client):
    # type: (str, docker.DockerClient) -> List[Network]

    stack_networks = list()
    network_list = client.networks.list(names=[stack_name])

    # TODO - Check if an exception is raised when the network has no labels
    stack_networks_id = [
        network.attrs["Id"]
        for network in network_list
        if network.attrs["Labels"]["com.docker.stack.namespace"] == stack_name
    ]
    for network in stack_networks_id:
        stack_networks.append(client.networks.get(network))
    return stack_networks
