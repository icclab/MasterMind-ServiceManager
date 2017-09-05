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
]


class Volume(object):
    def __init__(self,
                 name,
                 client=None,
                 driver=None,
                 options=None,
                 labels=None
                 ):
        self.client = client
        self.name = name
        self.driver = driver
        self.options = options
        self.labels = labels or {}

    def __repr__(self):
        return "<Network: {}>".format(self.name)

    def create(self):
        self.client.volumes.create(name=self.name,
                                   driver=self.driver,
                                   options=self.options,
                                   labels=self.labels)


def load_volumes(stack_name: str,
                 volume_dict: Dict,
                 cli: DockerClient) -> List[Volume]:

    volumes = list()
    for volume_name, volume_attr in volume_dict.items():
        volume_configuration_dict = get_volume_configuration(stack_name,
                                                             volume_attr)
        volume = Volume(
            name=stack_name + "_" + volume_name,
            client=cli,
            **volume_configuration_dict
        )
        volumes.append(volume)
    return volumes


def get_volume_configuration(stack_name: str,
                             config_dict: Dict) -> Dict:

    volume_attr_dict = dict()
    for key in VOLUME_KEYS:
        if key in config_dict:
            volume_attr_dict[key] = config_dict[key]

    volume_attr_dict["labels"] = dict()
    volume_attr_dict["labels"]["com.docker.stack.namespace"] = stack_name
    return volume_attr_dict
