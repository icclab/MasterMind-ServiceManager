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
from typing import (List, Dict)

from .exceptions import NetworkNotFound

NETWORK_KEYS = [
    "driver",
    "options",
    "ipam",
    "internal",
    "labels",
    "external"
]


class Network(object):
    def __init__(
            self,
            name,
            client=None,
            driver=None,
            external=False,
            options=None,
            ipam=None,
            check_duplicate=True,
            internal=False,
            labels=None,
            enable_ipv6=False,
    ):
        self.client = client
        self.name = name
        self.driver = driver
        self.external = external
        self.options = options
        self.ipam = ipam
        self.check_duplicate = check_duplicate
        self.internal = internal
        self.labels = labels or {}
        self.enable_ipv6 = enable_ipv6

    def __repr__(self):
        return "<Network: {}>".format(self.name)

    def create(self):
        if self.external:
            self.check_external_network()
        self.client.networks.create(name=self.name,
                                    driver=self.driver,
                                    options=self.options,
                                    ipam=self.ipam,
                                    check_duplicate=self.check_duplicate,
                                    internal=self.internal,
                                    labels=self.labels)

    def check_external_network(self):
        if not self.client.networks.list(names=self.name):
            raise NetworkNotFound


def load_networks(stack_name: str,
                  network_dict: Dict,
                  cli: DockerClient) -> List[Network]:

    networks = list()
    for network_name, network_attr in network_dict.items():
        network_configuration_dict = get_network_configuration(stack_name,
                                                               network_attr)
        network = Network(
            name=stack_name + "_" + network_name,
            client=cli,
            **network_configuration_dict
        )
        networks.append(network)
    return networks


def get_network_configuration(stack_name: str,
                              config_dict: Dict) -> Dict:
    network_attr_dict = dict()
    network_attr_dict["labels"] = dict()
    network_attr_dict["labels"]["com.docker.stack.namespace"] = stack_name

    for key in NETWORK_KEYS:
        if key in config_dict:
            network_attr_dict[key] = config_dict[key]
    # if hasattr(config_dict, "external"):
        # check_external_network()
    return network_attr_dict
