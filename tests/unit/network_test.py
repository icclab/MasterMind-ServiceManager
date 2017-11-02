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

import unittest

from .fake_api import MockDockerAPI
from swarm.network import Network


class NetworkTest(unittest.TestCase):
    def setUp(self):
        self.fake_client = MockDockerAPI()
        self.net_name = 'network'
        self.stack_name = 'stack'
        self.stack_label = {'com.docker.stack.namespace': self.stack_name}

    def test_network_with_stack_name(self):
        net = Network(name=self.net_name,
                      stack_name=self.stack_name)
        self.assertEquals(net.name, '{0}_{1}'.format(self.stack_name,
                                                     self.net_name))
        self.assertDictEqual(net.labels, self.stack_label)

    def test_network_labels_dict(self):
        labels = {'test': 'driver'}
        net = Network(name=self.net_name,
                      labels=labels)
        self.assertEquals(net.labels, labels)

    def test_network_labels_list(self):
        labels = ['test=driver']
        net = Network(name=self.net_name,
                      labels=labels)
        lbls = {'test': 'driver'}
        self.assertEquals(net.labels, lbls)
