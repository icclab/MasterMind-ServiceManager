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
from swarm.volume import Volume


class VolumeTest(unittest.TestCase):
    def setUp(self):
        self.fake_client = MockDockerAPI()
        self.vol_name = 'volume'
        self.stack_name = 'stack'
        self.stack_label = {'com.docker.stack.namespace': self.stack_name}

    def test_volume_with_stack_name(self):
        vol = Volume(name=self.vol_name,
                     stack_name=self.stack_name)
        self.assertEquals(vol.name, '{0}_{1}'.format(self.stack_name,
                                                     self.vol_name))
        self.assertDictEqual(vol.labels, self.stack_label)
