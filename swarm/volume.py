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


class Volume(object):
    def __init__(
            self,
            name,
            stack_name=None,
            driver=None,
            driver_opts=None,
            external=False,
            labels=None
    ):
        self.name = name
        self.stack_name = stack_name
        self.driver = driver
        self.driver_opts = driver_opts
        self.external = external
        self.labels = labels or {}
        self._initialize_volume()

    def __repr__(self):
        return "<Volume: {}>".format(self.name)

    def create(self, client) -> None:
        if not self.external:
            client.volumes.create(name=self.name,
                                  driver=self.driver,
                                  driver_opts=self.driver_opts,
                                  labels=self.labels)

    def _initialize_volume(self) -> None:
        if self.stack_name:
            if not self.external:
                self.name = '{0}_{1}'.format(self.stack_name, self.name)
            self.labels.update({"com.docker.stack.namespace": self.stack_name})
