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

import unittest

from .fake_compose_file import COMPOSE_WITHOUT_NETWORK_AND_VOLUMES, \
    COMPOSE_WITH_NETWORK_AND_VOLUMES
from .fake_api import MockDockerAPI
from swarm.stack import Stack
from swarm.service import Service
from swarm.network import Network
from swarm.volume import Volume


class StackTest(unittest.TestCase):
    def setUp(self):
        self.fake_client = MockDockerAPI()
        self.stack_name = 'stack'
        self.stack_label = {'com.docker.stack.namespace': self.stack_name}

    def test_create_stack_without_volumes_and_networks(self):
        compose = COMPOSE_WITHOUT_NETWORK_AND_VOLUMES
        stack = Stack(stack_name=self.stack_name,
                      compose_file=compose,
                      client=self.fake_client)
        svcs, nets, vols = stack.create()
        self.assertIsInstance(svcs, list)
        for svc in svcs:
            self.assertIsInstance(svc, Service)
            self.assertEquals(svc.name, 'stack_test')
            self.assertEquals(svc.image, 'test:1.13')
            self.assertEquals(svc.ports, ['8080:8080'])
            self.assertEquals(svc.environment, {'LABEL': 'Test'})
        self.assertIsInstance(nets, list)
        for net in nets:
            self.assertIsInstance(net, Network)
            self.assertEquals(net.name, 'stack_default')
        self.assertEquals(vols, [])

    def test_create_stack_with_volumes_and_networks(self):
        compose = COMPOSE_WITH_NETWORK_AND_VOLUMES
        stack = Stack(stack_name=self.stack_name,
                      compose_file=compose,
                      client=self.fake_client)
        svcs, nets, vols = stack.create()
        self.assertIsInstance(svcs, list)
        for svc in svcs:
            self.assertIsInstance(svc, Service)
            self.assertEquals(svc.name, 'stack_test')
            self.assertEquals(svc.image, 'test:1.13')
        self.assertIsInstance(nets, list)
        for net in nets:
            self.assertIsInstance(net, Network)
            self.assertIn(net.name, ['stack_backend', 'stack_default'])
        self.assertIsInstance(vols, list)
        for vol in vols:
            self.assertIsInstance(vol, Volume)
            self.assertEquals(vol.name, 'stack_test-volume')
