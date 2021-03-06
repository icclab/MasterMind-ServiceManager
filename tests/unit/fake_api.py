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


class MockDockerComponent:
    def __init__(self, name):
        self.name = name

    def list(self, names=None, filters=None):
        if names:
            for name in names:
                if name == self.name:
                    return [self]
            return []
        if filters:
            return []
        return [self]

    def create(self, *args, **kwargs):
        return self, args, kwargs


class MockDockerAPI:
    networks = MockDockerComponent(name='default')
    volumes = MockDockerComponent(name='test')
    services = MockDockerComponent(name='test')
