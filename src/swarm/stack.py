# Copyright (c) 2017. Zuercher Hochschule fuer Angewandte Wissenschaften
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
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
from .network import Network
from .service import Service
from .volume import Volume


def create(obj_list: List[Union[Volume, Network, Service]]) -> None:
    for obj in obj_list:
        obj.create()


def create_stack(stack_name: str,
                 compose_file: Dict,
                 client: DockerClient) -> List[Service]:

    if _get_stack_services(stack_name, client):
        raise StackNameExists('Stack name already in use.')

    network_list = list(
        map(lambda nt: _create_obj_from_dict(nt, Network, client, stack_name),
            compose_file.get('networks').items())
    ) if compose_file.get('networks') else _create_default_network(stack_name,
                                                                   client)
    create(network_list)

    volume_list = list(
        map(lambda vol: _create_obj_from_dict(vol, Volume, client, stack_name),
            compose_file.get('volumes').items())
    ) if compose_file.get('volumes') else []
    create(volume_list)

    service_list = list(
        map(lambda sv: _create_obj_from_dict(sv, Service, client, stack_name),
            compose_file.get('services').items())
    )if compose_file.get('services') else []
    create(service_list)
    return service_list


def remove_stack(stack_name: str, client: DockerClient) -> None:
    if not _get_stack_services(stack_name, client):
        raise StackNotFound('Stack not found.')

    service_list = _get_stack_services(stack_name, client)
    for service in service_list:
        service.remove()

    network_list = _get_stack_networks(stack_name, client)
    for network in network_list:
        network.remove()


def get_stack_health(stack_name: str, client: DockerClient) -> List[Dict]:
    service_list = _get_stack_services(stack_name, client)
    if not service_list:
        raise StackNotFound('Stack not found.')

    stack_status = list(map(_filter_service_info, service_list))
    return stack_status


def _create_obj_from_dict(dictionary, obj_class, client, stack_name):
    obj_name, obj_attrs = dictionary
    if not obj_attrs:
        obj_attrs = {}
    return obj_class(obj_name, client, stack_name=stack_name, **obj_attrs)


def _create_default_network(stack_name, client):
    net_name = "default"
    net = Network(net_name, client, stack_name=stack_name, driver="overlay")
    return [net]


def _filter_service_info(svc):
    svc_attrs = svc.attrs.get('Spec')
    service_tasks = svc.tasks()
    service_task_status = list(
        filter(
            lambda tsk: tsk.get('Status').get('State') == 'running',
            service_tasks
        )
    )
    return dict(
        name=svc_attrs.get('Name'),
        status='{0}/{1}'.format(
            len(service_task_status),
            svc_attrs.get('Mode').get('Replicated').get('Replicas')
        )
    )


def _get_stack_services(stack_name: str,
                        client: DockerClient) -> List[services.Service]:
    stack_service_ids = list()
    service_list = client.services.list(filters={'name': stack_name})

    for service in service_list:
        try:
            if service.attrs['Spec']['Labels']['com.docker.stack.namespace'] \
                    == stack_name:
                stack_service_ids.append(service.attrs['ID'])

        # Jump to the next service in the list in case the service doesn't have
        # the 'com.docker.stack.namespace' label
        except KeyError:
            continue

    stack_services = list(
        map(lambda svc_id: client.services.get(svc_id), stack_service_ids)
    )
    return stack_services


def _get_stack_networks(stack_name: str,
                        client: DockerClient) -> List[networks.Network]:
    stack_networks = list()
    stack_network_ids = list()
    network_list = client.networks.list(names=[stack_name])

    for network in network_list:
        try:
            if network.attrs['Labels']['com.docker.stack.namespace'] \
                    == stack_name:
                stack_network_ids.append(network.attrs['Id'])
        except KeyError:
            continue

    for network in stack_network_ids:
        stack_networks.append(client.networks.get(network))
    return stack_networks
