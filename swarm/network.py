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

from .exceptions import NetworkNotFound
from typing import Dict

IPAM_CONFIG_KEYS = [
    'driver',
    'options'
    'pool_configs'
]

IPAM_POOL_KEYS = [
    'subnet',
    'iprange',
    'gateway',
    'aux_addresses'
]


class Network(object):
    def __init__(
            self,
            name,
            client,
            stack_name=None,
            driver=None,
            external=False,
            check_duplicate=True,
            driver_options=None,
            ipam=None,
            internal=False,
            labels=None,
            enable_ipv6=False,
    ):
        self.name = name
        self.client = client
        self.stack_name = stack_name
        self.driver = driver
        self.external = external
        self.driver_options = driver_options
        self.ipam = ipam
        self.check_duplicate = check_duplicate
        self.internal = internal
        self.labels = labels or {}
        self.enable_ipv6 = enable_ipv6

        self._initialize_network()

    def __repr__(self):
        return "<Network: {}>".format(self.name)

    def create(self):
        self.client.networks.create(name=self.name,
                                    driver=self.driver,
                                    options=self.driver_options,
                                    ipam=self.ipam,
                                    check_duplicate=self.check_duplicate,
                                    internal=self.internal,
                                    labels=self.labels)

    def _initialize_network(self):
        self._network_labels()
        if self.external:
            self.check_external_network_exists()

        if self.stack_name:
            if not self.external:
                self.name = self.stack_name + "_" + self.name
            self.labels.update({'com.docker.stack.namespace': self.stack_name})

    def _network_labels(self):
        if isinstance(self.labels, list):
            def label_to_dict(label: str, dictionary: Dict):
                if "=" in label:
                    label_key, label_value = label.split("=")
                    dictionary[label_key] = label_value
                else:
                    dictionary[label] = ""

            lbls = self.labels
            self.labels = dict()
            map(lambda lbl: label_to_dict(lbl, self.labels), lbls)

    def check_external_network_exists(self):
        if not self.client.networks.list(names=self.name):
            raise NetworkNotFound("External network not found.")
