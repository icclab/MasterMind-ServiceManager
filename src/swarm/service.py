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

import enum

from docker.types.services import ServiceMode, EndpointSpec, RestartPolicy, \
    UpdateConfig, NetworkAttachment
from typing import (List, Dict)


UPDATE_CONFIG_KEYS = [
    'parallelism',
    'delay',
    'failure_action',
    'monitor',
    'max_failure_ratio'
]

RESTART_POLICY_KEYS = [
    'condition',
    'delay',
    'max_attempts',
    'window'
]


@enum.unique
class Modes(enum.Enum):
    """Enumeration for the types of service modes known to compose."""
    GLOBAL = "global"
    REPLICATED = "replicated"


class Service(object):
    def __init__(
            self,
            name,
            client,
            image=None,
            command=None,
            entrypoint=None,
            environment=None,
            hostname=None,
            labels=None,
            links=None,
            logging=None,
            volumes=None,
            networks=None,
            deploy=None,
            ports=None,
            stack_name=None,
            stop_grace_period=None,
            user=None,
            workdir=None
    ):
        self.command = command
        self.client = client
        self.deploy = deploy
        self.entrypoint = entrypoint
        self.environment = environment
        self.hostname = hostname
        self.links = links
        self.logging = logging
        self.image = image
        self.name = name
        self.networks = networks or ["default"]
        self.ports = ports
        self.stack_name = stack_name
        self.stop_grace_period = stop_grace_period
        self.user = user
        self.volumes = volumes
        self.workdir = workdir

        self.container_labels = dict()
        self.endpoint_spec = None
        self.service_labels = dict()
        self.log_driver = None
        self.log_driver_options = None
        self.mode = None
        self.restart_policy = None
        self.update_config = None
        self._initialize_service()
        self._service_container_labels(labels)

    def __repr__(self):
        return "<Service: {}>".format(self.name)

    def create(self):
        self.client.services.create(self.image,
                                    command=self.entrypoint,
                                    args=self.command,
                                    # constraints=self.constraints,
                                    container_labels=self.container_labels,
                                    endpoint_spec=self.endpoint_spec,
                                    env=self.environment,
                                    hostname=self.hostname,
                                    labels=self.service_labels,
                                    log_driver=self.log_driver,
                                    log_driver_options=self.log_driver_options,
                                    mode=self.mode,
                                    name=self.name,
                                    networks=self.networks,
                                    restart_policy=self.restart_policy,
                                    stop_grace_period=self.stop_grace_period,
                                    update_config=self.update_config,
                                    user=self.user,
                                    workdir=self.workdir)

    def _initialize_service(self):

        self._check_network_names()
        if self.ports:
            self._service_endpoint_specs(self.ports)

        if self.stack_name:
            self.service_labels.update(
                {'com.docker.stack.namespace': self.stack_name}
            )

        self.name = self.stack_name + "_" + self.name if self.stack_name \
            else self.name

        if self.deploy and self.deploy.get('labels'):
            self._service_labels(
                self.deploy.get('labels')
            )

        if self.command and isinstance(self.command, str):
            self.command = self.command.split()

        if self.deploy and self.deploy.get('restart_policy'):
            self._service_restart_policy(
                self.deploy.get('restart_policy')
            )

        if self.deploy and self.deploy.get('update_config'):
            self._service_update_config(
                self.deploy.get('update_config')
            )

        if self.deploy and \
                (self.deploy.get('mode') or self.deploy.get('replicas')):
            self._service_mode(
                self.deploy
            )

    def _check_network_names(self):
        prefix = self.stack_name + "_"
        networks = [
            prefix + network if prefix + network in list(
                map(
                    lambda netw: netw.name,
                    self.client.networks.list(names=[self.stack_name])
                )
            )
            else network for network in self.networks
        ]
        self.networks = list(map(
            lambda net: NetworkAttachment(network=net, aliases=[self.name]),
            networks
        ))

    def _service_endpoint_specs(self, ports: List[str]) -> None:
        ports_dict = dict()
        for p in ports:
            p_str = p.split(":")
            ports_dict[int(p_str[0])] = int(p_str[1])
        self.endpoint_spec = EndpointSpec(ports=ports_dict)

    def _service_mode(self, mode: Dict) -> None:
        svc_mode = mode.get('mode') or Modes.REPLICATED
        svc_replicas = mode.get('replicas') or 1 \
            if svc_mode != Modes.GLOBAL else None
        self.mode = ServiceMode(mode=svc_mode, replicas=svc_replicas)

    def _service_update_config(self, update_config_dict: Dict) -> None:
        check_dict_keys(update_config_dict, UPDATE_CONFIG_KEYS)
        self.update_config = UpdateConfig(**update_config_dict)

    def _service_restart_policy(self, restart_policy_dict: Dict) -> None:
        check_dict_keys(restart_policy_dict, RESTART_POLICY_KEYS)
        self.restart_policy = RestartPolicy(**restart_policy_dict)

    def _service_container_labels(self, labels) -> None:
        if isinstance(labels, dict):
            self.container_labels = labels
        elif isinstance(labels, list):
            label_dict = dict()
            for label in labels:
                try:
                    label_key, label_value = label.split("=")
                    label_dict[label_key] = label_value
                # ValueError raised for labels without value
                except ValueError:
                    label_dict[label] = ""
            self.container_labels = label_dict
        if self.stack_name:
            self.container_labels.update(
                {'com.docker.stack.namespace': self.stack_name}
            )

    def _service_labels(self, labels):
        self.service_labels.update(labels)

    def _service_logs(self, logging: Dict):
        pass


def check_dict_keys(dictionary: Dict, valid_keys: List[str]) -> None:
    [dictionary.pop(key) for key in dictionary.keys() if key not in valid_keys]
