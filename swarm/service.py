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
from docker.types.services import ServiceMode, EndpointSpec, RestartPolicy, \
    UpdateConfig, NetworkAttachment
from typing import List, Dict, Text


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

SECRET_KEYS = [
    'source',
    'target',
    'uid',
    'gid',
    'mode'
]


class Modes(object):
    """Enumeration for the types of service modes known to compose."""
    GLOBAL = "global"
    REPLICATED = "replicated"


class Service(object):
    def __init__(
            self,
            name,
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
            secrets=None,
            stack_name=None,
            stop_grace_period=None,
            user=None,
            workdir=None
    ):
        self.command = command
        self.deploy = deploy
        self.entrypoint = entrypoint
        self.environment = environment
        self.hostname = hostname
        self.links = links
        self.logging = logging
        self.image = image
        self.name = name
        self.networks = networks or []
        self.ports = ports
        self.secrets = secrets
        self.stack_name = stack_name or ''
        self.stop_grace_period = stop_grace_period
        self.user = user
        self.volumes = volumes
        self.workdir = workdir

        self.container_labels = {}
        self.endpoint_spec = None
        self.service_labels = {}
        self.log_driver = None
        self.log_driver_options = None
        self.mode = None
        self.network_attachments = None
        self.restart_policy = None
        self.update_config = None
        self._initialize_service()
        self._service_container_labels(labels)

    def __repr__(self):
        return "<Service: {}>".format(self.name)

    def create(self, client: DockerClient):
        client.services.create(self.image,
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
                               networks=self.network_attachments,
                               restart_policy=self.restart_policy,
                               stop_grace_period=self.stop_grace_period,
                               update_config=self.update_config,
                               user=self.user,
                               workdir=self.workdir)

    def _initialize_service(self):
        self._check_network_exists()
        if self.ports:
            self._service_endpoint_specs(self.ports)

        if self.stack_name:
            stack_label = {'com.docker.stack.namespace': self.stack_name}
            self.service_labels.update(stack_label)
            self.container_labels.update(stack_label)
            self.name = '{0}_{1}'.format(self.stack_name, self.name)

        if self.deploy:
            if self.deploy.get('labels'):
                self._service_labels(self.deploy.get('labels'))
            if self.deploy.get('restart_policy'):
                self._service_restart_policy(self.deploy.get('restart_policy'))
            if self.deploy.get('update_config'):
                self._service_update_config(self.deploy.get('update_config'))
            if self.deploy.get('mode') or self.deploy.get('replicas'):
                self._service_mode(self.deploy)
        if self.command and isinstance(self.command, Text):
            self.command = self.command.split()
        if self.secrets:
            pass

    def _check_network_exists(self):
        if self.networks and isinstance(self.networks, list):
            self.network_attachments = list(map(
                lambda nt: NetworkAttachment(network=nt, aliases=[self.name]),
                self.networks
            ))
        else:
            default_net = '{0}_{1}'.format(self.stack_name, 'default')
            self.network_attachments = [
                NetworkAttachment(network=default_net, aliases=[self.name])
            ]

    def _service_endpoint_specs(self, ports: List[str]) -> None:
        ports_dict = dict()
        for p in ports:
            p_host, p_container = p.split(":")
            ports_dict[int(p_host)] = int(p_container)
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
            self.container_labels.update(labels)
        elif isinstance(labels, list):
            def label_to_dict(label: str):
                if "=" in label:
                    label_key, label_value = label.split('=')
                    return {label_key: label_value}
                else:
                    return {label: ''}
            label_dict = dict()
            lbs = list(map(lambda lbl: label_to_dict(lbl), labels))
            for lb in lbs:
                label_dict.update(lb)
            self.container_labels.update(label_dict)

    def _service_labels(self, labels):
        self.service_labels.update(labels)


def check_dict_keys(dictionary: Dict, valid_keys: List[str]) -> None:
    dikt = dictionary.copy()
    [dictionary.pop(key) for key in dikt.keys() if key not in valid_keys]
