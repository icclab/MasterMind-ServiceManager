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

from docker import DockerClient
from typing import Dict


def get_swarm_status(docker_client: DockerClient) -> Dict:
    def get_node_list_by_role(role: str):
        return docker_client.nodes.list(filters={'role': role})

    manager_list = list(
        map(_filter_node_info, get_node_list_by_role('manager'))
    )
    worker_list = list(
        map(_filter_node_info, get_node_list_by_role('worker'))
    )
    return {'managers': manager_list, 'workers': worker_list}


def _filter_node_info(node):
    return dict(
        resources=node.attrs.get("Description").get("Resources"),
        availability=node.attrs.get("Spec").get("Availability"),
        hostname=node.attrs.get("Description").get("Hostname"),
        address=node.attrs.get("Status").get("Addr")
    )
