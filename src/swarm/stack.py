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

from __future__ import absolute_import
from typing import List, Dict, Union

from docker import DockerClient
from docker.models import services, networks

from .exceptions import StackNameExists, StackNotFound
from .network import Network, load_networks
from .service import Service, load_services
from .volume import Volume, load_volumes


def create(obj_list: List[Union[Volume, Network, Service]],
           client: DockerClient) -> None:
    for obj in obj_list:
        obj.create(client)


def create_stack(stack_name: str,
                 compose_file: Dict,
                 client: DockerClient) -> List[Service]:

    service_list = list()

    # Check if stack_name is already in use
    if get_stack_services(stack_name, client):
        raise StackNameExists("Stack name already in use.")

    if compose_file.get("networks"):
        network_list = load_networks(
            stack_name,
            compose_file.get("networks"),
            client
        )
        create(network_list, client)

    if compose_file.get("volumes"):
        volume_list = load_volumes(
            stack_name,
            compose_file.get('volumes')
        )
        create(volume_list, client)

    if compose_file.get("services"):
        service_list = load_services(
            stack_name,
            compose_file.get("services")
        )
        create(service_list, client)
    return service_list


def remove_stack(stack_name: str, client: DockerClient) -> None:
    if not get_stack_services(stack_name, client):
        raise StackNotFound("Stack not found.")

    service_list = get_stack_services(stack_name, client)
    for service in service_list:
        service.remove()

    network_list = get_stack_networks(stack_name, client)
    for network in network_list:
        network.remove()


def get_stack_health(stack_name: str, client: DockerClient) -> List[Dict]:
    if not get_stack_services(stack_name, client):
        raise StackNotFound("Stack not found.")

    service_list = get_stack_services(stack_name, client)

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


def get_stack_services(stack_name: str,
                       client: DockerClient) -> List[services.Service]:
    stack_services = list()
    stack_service_ids = list()
    service_list = client.services.list(filters={'name': stack_name})

    for service in service_list:
        try:
            if service.attrs["Spec"]["Labels"]["com.docker.stack.namespace"] \
                    == stack_name:
                stack_service_ids.append(service.attrs["ID"])

        # Jump to the next service in the list in case the service doesn't have
        # the "com.docker.stack.namespace" label
        except KeyError:
            continue

    for service in stack_service_ids:
        stack_services.append(client.services.get(service))
    return stack_services


def get_stack_networks(stack_name: str,
                       client: DockerClient) -> List[networks.Network]:
    stack_networks = list()
    stack_network_ids = list()
    network_list = client.networks.list(names=[stack_name])

    for network in network_list:
        try:
            if network.attrs["Labels"]["com.docker.stack.namespace"] \
                    == stack_name:
                stack_network_ids.append(network.attrs["Id"])
        except KeyError:
            continue

    for network in stack_network_ids:
        stack_networks.append(client.networks.get(network))
    return stack_networks
