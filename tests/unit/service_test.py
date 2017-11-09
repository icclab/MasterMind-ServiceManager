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
from docker.types.services import ServiceMode, EndpointSpec, UpdateConfig, \
    RestartPolicy
from swarm.service import Service


class ServiceTest(unittest.TestCase):
    def setUp(self):
        self.fake_client = MockDockerAPI()
        self.svc_name = 'service'
        self.stack_name = 'stack'
        self.stack_label = {'com.docker.stack.namespace': self.stack_name}

    def test_service_with_stack_name(self):
        svc = Service(name=self.svc_name,
                      stack_name=self.stack_name)
        self.assertEquals(svc.name, '{0}_{1}'.format(self.stack_name,
                                                     self.svc_name))
        self.assertDictEqual(svc.container_labels, self.stack_label)
        self.assertDictEqual(svc.service_labels, self.stack_label)

    def test_service_ports(self):
        ports = ['8080:8080']
        svc = Service(name=self.svc_name,
                      ports=ports)
        endpoint_spec = EndpointSpec(ports={8080: 8080})
        self.assertEquals(svc.endpoint_spec, endpoint_spec)

    def test_service_replicas(self):
        replicas = {'replicas': 3}
        svc = Service(name=self.svc_name,
                      deploy=replicas)
        svc_mode = ServiceMode('replicated', 3)
        self.assertEquals(svc.mode, svc_mode)

    def test_service_global_mode(self):
        mode = {'mode': 'global'}
        svc = Service(name=self.svc_name,
                      deploy=mode)
        svc_mode = ServiceMode('global')
        self.assertEquals(svc.mode, svc_mode)

    def test_service_labels_with_stack_name(self):
        labels = {'labels': {'test': 'driver'}}
        svc = Service(name=self.svc_name,
                      deploy=labels,
                      stack_name=self.stack_name)
        svc_labels = {}
        svc_labels.update(labels.get('labels'))
        svc_labels.update(self.stack_label)

        self.assertEquals(svc.service_labels, svc_labels)

    def test_service_update_config(self):
        update_config = {'update_config': {'parallelism': 2,
                                           'delay': '3s',
                                           'monitor': '5s',
                                           'failure_action': 'continue',
                                           'max_failure_ratio': 0.1}}
        svc = Service(name=self.svc_name,
                      deploy=update_config)
        updt_config = UpdateConfig(parallelism=2, delay=3, monitor=5000000000,
                                   failure_action='continue',
                                   max_failure_ratio=0.1)

        self.assertEquals(svc.update_config, updt_config)

    def test_service_restart_policy(self):
        restart_policy = {'restart_policy': {'condition': 'none',
                                             'delay': '3s',
                                             'max_attempts': 5,
                                             'window': 0}}
        svc = Service(name=self.svc_name,
                      deploy=restart_policy)
        rest_config = RestartPolicy(condition='none', delay=3, max_attempts=5,
                                    window=0)

        self.assertEquals(svc.restart_policy, rest_config)

    def test_service_restart_policy_with_additional_parameters(self):
        restart_policy = {'restart_policy': {'condition': 'none',
                                             'delay': '3s',
                                             'max_attempts': 5,
                                             'test': 'unused_parameter'}}
        svc = Service(name=self.svc_name,
                      deploy=restart_policy)
        rest_config = RestartPolicy(condition='none', delay=3, max_attempts=5,
                                    window=0)

        self.assertEquals(svc.restart_policy, rest_config)

    def test_service_container_labels_dict(self):
        labels = {'test': 'driver'}
        svc = Service(name=self.svc_name,
                      labels=labels)
        self.assertEquals(svc.container_labels, labels)

    def test_service_container_labels_list(self):
        labels = ['test=driver']
        svc = Service(name=self.svc_name,
                      labels=labels)
        lbls = {'test': 'driver'}
        self.assertEquals(svc.container_labels, lbls)
