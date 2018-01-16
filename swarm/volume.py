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
import docker.errors
import logging

logger = logging.getLogger(__name__)


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

    def create(self, client: DockerClient) -> None:
        if not self.external:
            client.volumes.create(name=self.name,
                                  driver=self.driver,
                                  driver_opts=self.driver_opts,
                                  labels=self.labels)

    def remove(self, client: DockerClient) -> bool:
        try:
            v = client.volumes.get(volume_id=self.name)
            v.remove()
            return True
        except docker.errors.APIError:
            # TODO(murp): need to perform more intelligent error handling here.
            return False

    def _initialize_volume(self) -> None:
        if self.stack_name:
            if not self.external:
                self.name = '{0}_{1}'.format(self.stack_name, self.name)
            self.labels.update({"com.docker.stack.namespace": self.stack_name})


def remove_volume(vol_name: str, client: DockerClient) -> bool:
    '''Removes volume of given name from engine pointed to by client'''
    try:
        logger.debug("About to remove volume {0}".format(vol_name))
        v = client.volumes.get(volume_id=vol_name)
        logger.debug("Volume: {0}".format(v))
        v.remove()
        logger.info("Successfully removed volume {0}".format(vol_name))
        return True
    except docker.errors.APIError as err:
        # TODO(murp): need to perform more intelligent error handling here.
        logger.info("Problem removing volume {0} - error message: {1}"
                    .format(vol_name, err))
        return False
