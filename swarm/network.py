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
            stack_name=None,
            driver=None,
            external=False,
            check_duplicate=True,
            driver_opts=None,
            ipam=None,
            internal=False,
            labels=None,
            enable_ipv6=False,
            **options
    ):
        self.name = name
        self.stack_name = stack_name
        self.driver = driver
        self.external = external
        self.driver_options = driver_opts
        self.ipam = ipam
        self.check_duplicate = check_duplicate
        self.internal = internal
        self.labels = labels or {}
        self.enable_ipv6 = enable_ipv6
        self.options = options

        self._initialize_network()

    def __repr__(self):
        return "<Network: {}>".format(self.name)

    def create(self, client: DockerClient):
        client.networks.create(name=self.name,
                               driver=self.driver,
                               options=self.driver_options,
                               ipam=self.ipam,
                               check_duplicate=self.check_duplicate,
                               internal=self.internal,
                               labels=self.labels)

    def _initialize_network(self):
        self._network_labels()

        if self.stack_name:
            if not self.external:
                self.name = '{0}_{1}'.format(self.stack_name, self.name)
            self.labels.update({'com.docker.stack.namespace': self.stack_name})
        if self.driver_options:
            opts = self.driver_options.copy()
            for key, value in opts.items():
                self.driver_options[key] = str(value)

    def _network_labels(self):
        if isinstance(self.labels, list):
            def label_to_dict(label: str):
                if "=" in label:
                    label_key, label_value = label.split('=')
                    return {label_key: label_value}
                else:
                    return {label: ''}
            label_dict = dict()
            lbs = list(map(lambda lbl: label_to_dict(lbl), self.labels))
            for lb in lbs:
                label_dict.update(lb)
            self.labels = label_dict
