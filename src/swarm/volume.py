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
from typing import (List, Dict)

VOLUME_KEYS = [
    "driver",
    "driver_opts",
    "labels"
    "external"
]


class Volume(object):
    def __init__(
            self,
            name,
            client=None,
            driver=None,
            driver_opts=None,
            labels=None
    ):
        self.client = client
        self.name = name
        self.driver = driver
        self.driver_opts = driver_opts
        self.labels = labels or {}

    def __repr__(self):
        return "<Network: {}>".format(self.name)

    def create(self):
        self.client.volumes.create(name=self.name,
                                   driver=self.driver,
                                   driver_opts=self.driver_opts,
                                   labels=self.labels)


def load_volumes(stack_name: str,
                 volume_dict: Dict,
                 cli: DockerClient) -> List[Volume]:

    volumes = list()
    for volume_name, volume_attr in volume_dict.items():
        volume_configuration_dict = set_volume_configuration(stack_name,
                                                             volume_attr)
        volume = Volume(
            name=stack_name + "_" + volume_name,
            client=cli,
            **volume_configuration_dict
        )
        volumes.append(volume)
    return volumes


def set_volume_configuration(stack_name: str,
                             config_dict: Dict) -> Dict:

    volume_attr_dict = dict()
    volume_attr_dict["labels"] = dict()
    volume_attr_dict["labels"]["com.docker.stack.namespace"] = stack_name

    if config_dict:
        for key in VOLUME_KEYS:
            if key in config_dict:
                volume_attr_dict[key] = config_dict[key]

    return volume_attr_dict
