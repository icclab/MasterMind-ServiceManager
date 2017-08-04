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

NETWORK_KEYS = [
    "driver",
    "options",
    "ipam",
    "internal",
    "labels",
    "external"
]


class Network(object):
    def __init__(self,
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
                 stack_name=None):
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
        self.stack_name = stack_name

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
            raise NotImplementedError
