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
from docker.types.healthcheck import Healthcheck
from typing import List, Dict, Text
from docker.errors import APIError

from .utils import convert_time_to_secs, convert_time_to_nano_secs

import logging

logger = logging.getLogger(__name__)


class Modes(object):
    """Enumeration for the types of service modes known to compose."""
    GLOBAL = "global"
    REPLICATED = "replicated"


class Service(object):
    """
    This class is only used for creating services in a Stack.
    Each services defined in the compose-file are passed to this class as
    a dictionary which is then processed in order to match the docker-py lib.
    """
    def __init__(
            self,
            name,
            image=None,
            command=None,
            configs=None,
            entrypoint=None,
            environment=None,
            healthcheck=None,
            hostname=None,
            labels=None,
            logging=None,
            volumes=None,
            networks=None,
            deploy=None,
            ports=None,
            secrets=None,
            stack_name=None,
            stop_grace_period=None,
            user=None,
            workdir=None,
            **options
    ):
        self.command = command
        self.configs = configs
        self.deploy = deploy
        self.entrypoint = entrypoint
        self.environment = environment
        self.healthcheck = healthcheck
        self.hostname = hostname
        self.logging = logging
        self.image = image
        self.name = name
        self.networks = networks or []
        self.options = options
        self.ports = ports
        self.secrets = secrets
        self.stack_name = stack_name or ''
        self.stop_grace_period = stop_grace_period
        self.user = user
        self.volumes = volumes
        self.workdir = workdir

        self.container_labels = {}
        self.constraints = None
        self.endpoint_spec = None
        self.service_labels = {}
        self.mode = None
        self.network_attachments = None
        self.restart_policy = None
        self.update_config = None
        self._initialize_service()
        self._service_container_labels(labels)

    def __repr__(self):
        return "<Service: {}>".format(self.name)

    def create(self, client: DockerClient) -> bool:
        try:
            client.services.create(self.image,
                                   command=self.entrypoint,
                                   args=self.command,
                                   constraints=self.constraints,
                                   container_labels=self.container_labels,
                                   endpoint_spec=self.endpoint_spec,
                                   env=self.environment,
                                   healthcheck=self.healthcheck,
                                   hostname=self.hostname,
                                   labels=self.service_labels,
                                   mode=self.mode,
                                   mounts=self.volumes,
                                   name=self.name,
                                   networks=self.network_attachments,
                                   restart_policy=self.restart_policy,
                                   secrets=self.secrets,
                                   stop_grace_period=self.stop_grace_period,
                                   update_config=self.update_config,
                                   user=self.user,
                                   workdir=self.workdir,
                                   configs=self.configs)
            return True
        except APIError as err:
            logger.info("Error creating service {0} - error message: {1}"
                        .format(self.name, err))
            return False

    def remove(self, client: DockerClient) -> bool:
        try:
            filters = {'name': self.name}
            service_list = client.services.list(filters=filters)
            # add logic to handle case in which no service is found...
            service_list[0].remove()
            return True
        except APIError as err:
            # TODO(murp): need to perform more intelligent error handling here.
            logger.info("Error removing service {0} - err msg: {1}"
                        .format(self.name, err))
            return False

    def _initialize_service(self):
        self._service_networks()
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
            if self.deploy.get('placement'):
                constraints = self.deploy.get('placement').get('constraints')
                if constraints and isinstance(constraints, list):
                    self.constraints = constraints
        if self.command and isinstance(self.command, Text):
            self.command = self.command.split()
        if self.healthcheck:
            self._service_healthcheck()
        if self.volumes:
            self._service_volumes()

    def _service_networks(self):
        """
        Check if there is any network associated with the service, if so it
        will create a list of NetworkAttachments adding the network name and
        the service name. The aliases parameter in NetworkAttachments allow the
        container to be reachable in the same network by its name as defined in
        the compose-file.
        In case the container does not have any network associated, it will
        attach the default network to it - which was create in the Stack class.
        """
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
        """
        Converts the 'ports' parameter in the compose-file into a EndpointSpec
        class as expected by docker-py lib. The only syntax supported is:
        - "8080:8080"
        """
        ports_dict = dict()
        for p in ports:
            p_host, p_container = p.split(":")
            ports_dict[int(p_host)] = int(p_container)
        self.endpoint_spec = EndpointSpec(ports=ports_dict)

    def _service_mode(self, mode: Dict) -> None:
        """
        Converts a couple of parameters - deploy['mode'] and deploy['replicas']
        into a ServiceMode class as expected by docker-py lib.
        Defaults to a 'replicated' service with 1 replica.
        """
        svc_mode = mode.get('mode') or Modes.REPLICATED
        svc_replicas = mode.get('replicas') or 1 \
            if svc_mode != Modes.GLOBAL else None
        self.mode = ServiceMode(mode=svc_mode, replicas=svc_replicas)

    def _service_update_config(self, update_cfg_dict: Dict) -> None:
        """
        Converts the parameters in deploy[update_config] into a UpdateConfig
        class as expected by docker-py lib.
        """
        self.update_config = UpdateConfig(
            parallelism=update_cfg_dict.get('parallelism') or 0,
            delay=convert_time_to_secs(update_cfg_dict.get('delay')) or None,
            failure_action=update_cfg_dict.get('failure_action') or 'continue',
            monitor=convert_time_to_nano_secs(
                update_cfg_dict.get('monitor')
            ) or None,
            max_failure_ratio=update_cfg_dict.get('max_failure_ratio') or None
        )

    def _service_restart_policy(self, restart_policy_dict: Dict) -> None:
        """
        Converts the parameters in deploy[restart_policy] into a RestartPolicy
        class as expected by docker-py lib.
        """
        self.restart_policy = RestartPolicy(
            condition=restart_policy_dict.get('condition') or 'none',
            delay=convert_time_to_secs(restart_policy_dict.get('delay')) or 0,
            max_attempts=restart_policy_dict.get('max_attempts') or 0,
            window=convert_time_to_secs(restart_policy_dict.get('window')) or 0
        )

    def _service_container_labels(self, labels) -> None:
        """
        Checks if the labels parameter - do not confuse with deploy[labels] -
        is either a dict or a list of strings. If it is a dictionary it will
        just update self.container_labels, else it will convert the list of
        strings to a dictionary.
        """
        if isinstance(labels, dict):
            self.container_labels.update(labels)
        elif isinstance(labels, list):
            def label_to_dict(label: str):
                # String labels usually have 'key=value' format, but it could
                # also happen to be just a 'key' without value - in this case
                # we add an empty value to the label.
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
        """
        Adds the contents of deploy[labels] to service_labels.
        """
        self.service_labels.update(labels)

    def _service_healthcheck(self):
        """
        Converts the parameters in healthcheck into a Healthcheck
        class as expected by docker-py lib.
        """
        healthcheck = self.healthcheck.copy()
        self.healthcheck = Healthcheck(
            test=healthcheck.get('test'),
            interval=convert_time_to_nano_secs(
                healthcheck.get('interval')
            ) or 0,
            timeout=convert_time_to_nano_secs(
                healthcheck.get('timeout')
            ) or 0,
            retries=healthcheck.get('retries'),
            start_period=convert_time_to_nano_secs(
                healthcheck.get('start_period')
            ) or 0
        )

    def _service_volumes(self):
        """
        Converts the list of strings provided for volumes into a list of
        strings expected by docker-py lib. This string should have the format -
        'volume_name:path_in_container:rw|ro'.
        """
        if isinstance(self.volumes, list):
            volumes = self.volumes.copy()
            for volume in volumes:
                volume_str_list = volume.split(':')
                if len(volume_str_list) == 1:
                    self.volumes[self.volumes.index(volume)] = \
                        '{0}:{1}:{2}'.format(volume, volume, ':rw')
                elif len(volume_str_list) == 2:
                    self.volumes[self.volumes.index(volume)] = volume + ':rw'
