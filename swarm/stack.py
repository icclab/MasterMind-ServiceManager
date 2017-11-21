# Copyright (c) 2017. Zuercher Hochschule fuer Angewandte Wissenschaften
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# AUTHOR: Bruno Grazioli

from __future__ import absolute_import
from typing import Dict, Union, Tuple, List, Iterable
from docker import DockerClient
from docker.models import services, networks
from docker.types.services import SecretReference, ConfigReference

from .exceptions import NetworkNotFound, VolumeNotFound, SecretNotFound, \
    ConfigNotFound
from .network import Network
from .service import Service
from .volume import Volume


class Stack(object):
    def __init__(self,
                 stack_name: str=None,
                 compose_file: Dict=None,
                 client: DockerClient=None):
        self.stack_name = stack_name
        self.compose_file = compose_file
        self.client = client

        self.default_network_created = False
        self.stack_networks = []
        self.services = []
        self.networks = []
        self.volumes = []
        self.service_dict = {}
        self.network_dict = {}
        self.volume_dict = {}

    def create(self) -> Tuple[List[Service], List[Network], List[Volume]]:
        """
        Creates a Stack - POST /v1/stack/
        """
        self.service_dict = self.compose_file.get('services')
        self.network_dict = self.compose_file.get('networks') or {}
        self.volume_dict = self.compose_file.get('volumes') or {}

        self._create_networks()
        self._create_volumes()
        self._create_services()
        return self.services, self.networks, self.volumes

    def remove(self) -> None:
        """
        Deletes a Stack - POST /v1/stack/delete/{name}
        Volumes are not deleted.
        """
        svc_list = self._get_stack_services()
        net_list = self._get_stack_networks()

        for svc in svc_list:
            svc.remove()
        for net in net_list:
            net.remove()

    def health(self) -> List[Dict]:
        """
        Gets a stack status - POST /v1/stack/{name}
        Returns Services associated to a Stack and their status -
        amount of active replicas / total amount of replicas it should have.
        """
        svc_list = self._get_stack_services()
        svcs = list(map(
            self._filter_service_info,
            svc_list
        ))
        return svcs

    def _create_networks(self) -> None:
        """
        Creates networks required by the Stack, it also checks if a service
        does not have networks associated to it. If so it will create a
        'default_{stack_name}' network for that service.
        This function also checks if the network is external and if it exists.
        """
        def check_if_network_is_external(net_tuple: Tuple):
            net_name, net_attrs = net_tuple
            if not net_attrs:
                net_attrs = {}
            if not net_attrs.get('external'):
                # This variable keeps track of all networks which are
                # not external
                self.stack_networks.append(net_name)
                return Network(net_name,
                               stack_name=self.stack_name,
                               **net_attrs)
            if not self.client.networks.list(names=[net_name]):
                raise NetworkNotFound(
                            "External network {0} not found.".format(net_name)
                )
            return net_name
        self.networks = list(map(
            lambda nt: check_if_network_is_external(nt),
            self.network_dict.items()
        ))
        for net in self.networks:
            if isinstance(net, Network):
                net.create(self.client)

    def _create_default_network(self) -> None:
        """
        Creates the default network for services without networks defined.
        """
        default_net = Network(name='default',
                              stack_name=self.stack_name,
                              driver='overlay')
        default_net.create(self.client)
        self.networks.append(default_net)

    def _create_volumes(self) -> None:
        """
        Creates volumes required by the Stack.
        This function also checks if the volume is external and if it exists.
        """
        def check_if_volume_is_external(vol_tuple: Tuple):
            vol_name, vol_attrs = vol_tuple
            if not vol_attrs:
                vol_attrs = {}
            if not vol_attrs.get('external'):
                return Volume(vol_name,
                              stack_name=self.stack_name,
                              **vol_attrs)
            if not self.client.volumes.list(filters={'name': vol_name}):
                raise VolumeNotFound(
                    "External volume {0} not found.".format(vol_name)
                )
            return vol_name
        self.volumes = list(map(
            lambda vl: check_if_volume_is_external(vl),
            self.volume_dict.items()
        ))
        for vol in self.volumes:
            if isinstance(vol, Volume):
                vol.create(self.client)

    def _create_services(self) -> None:

        self._check_stack_service_attributes()

        self.services = list(map(
            lambda sc: self._create_svc_from_tuple(sc),
            self.service_dict.items()
        ))
        for svc in self.services:
            if isinstance(svc, Service):
                svc.create(self.client)

    def _check_stack_service_attributes(self) -> None:
        for svc_name, svc_attrs in self.service_dict.items():
            self._parse_stack_service_networks(svc_attrs.get('networks') or [])
            self._parse_stack_service_secrets(svc_attrs.get('secrets') or [])
            self._parse_stack_service_configs(svc_attrs.get('configs') or [])

    def _parse_stack_service_networks(self, nets: Union[List, Dict]) -> None:
        """
        Check the networks associated with the service, if the network is
        not external then it will prepend the stack_name to the network name.
        """
        if isinstance(nets, list):
            nets_copy = nets.copy()
            for net in nets_copy:
                if net in self.stack_networks:
                    nets[nets.index(net)] = '{0}_{1}'.format(
                        self.stack_name, net
                    )
            if not nets:
                # Other service in the stack might have created the default
                # network.
                if not self.default_network_created:
                    self._create_default_network()
                    self.default_network_created = True

    def _parse_stack_service_secrets(self, secrets: List) -> None:
        """
        Checks if there is any Secret associated to the service,
        if so it retrieves the id of the secret and creates a SecretReference
        as expected by the docker-py lib.
        """
        def get_secret_id(scrt_name: str):
            scrt = self.client.secrets.list(filters={'names': scrt_name})
            if not scrt:
                raise SecretNotFound('Secret {0} not found'.format(scrt_name))
            if len(scrt) == 1:
                return scrt[0].id

        secrets_copy = secrets.copy()
        for secret in secrets_copy:
            if isinstance(secret, str):
                secret_id = get_secret_id(secret)
                secrets[secrets.index(secret)] = SecretReference(
                    secret_id=secret_id,
                    secret_name=secret
                )
            elif isinstance(secret, dict):
                secret_id = get_secret_id(secret.get('source'))
                secrets[secrets.index(secret)] = SecretReference(
                    secret_id=secret_id,
                    secret_name=secret.get('source'),
                    filename=secret.get('target'),
                    uid=secret.get('uid') or 0,
                    gid=secret.get('gid') or 0,
                    mode=secret.get('mode') or 0o444
                )

    def _parse_stack_service_configs(self, configs: List) -> None:
        """
        Checks if there is any Config associated to the service,
        if so it retrieves the id of the config and creates a ConfigReference
        as expected by the docker-py lib.
        """
        def get_config_id(cnfg_name: str):
            cnfg = self.client.configs.list(filters={'names': cnfg_name})
            if not cnfg:
                raise ConfigNotFound('Config {0} not found'.format(cnfg_name))
            if len(cnfg) == 1:
                return cnfg[0].id

        configs_copy = configs.copy()
        for config in configs_copy:
            if isinstance(config, str):
                config_id = get_config_id(config)
                configs[configs.index(config)] = ConfigReference(
                    config_id=config_id,
                    config_name=config
                )
            elif isinstance(config, dict):
                config_id = get_config_id(config.get('source'))
                configs[configs.index(config)] = ConfigReference(
                    config_id=config_id,
                    config_name=config.get('source'),
                    filename=config.get('target'),
                    uid=config.get('uid') or 0,
                    gid=config.get('gid') or 0,
                    mode=config.get('mode') or 0o444
                )

    def _create_svc_from_tuple(self, dict_tuple: Tuple,) -> Service:
        obj_name, obj_attrs = dict_tuple
        if not obj_attrs:
            obj_attrs = {}
        return Service(obj_name, stack_name=self.stack_name, **obj_attrs)

    def _get_stack_services(self) -> Iterable[services.Service]:
        filter_lbl = 'com.docker.stack.namespace={0}'.format(self.stack_name)
        return self.client.services.list(filters={'label': filter_lbl})

    def _get_stack_networks(self) -> Iterable[networks.Network]:
        filter_lbl = 'com.docker.stack.namespace={0}'.format(self.stack_name)
        return self.client.networks.list(filters={'label': filter_lbl})

    @staticmethod
    def _filter_service_info(svc: services.Service) -> Dict:
        svc_attrs = svc.attrs.get('Spec')
        service_tasks = svc.tasks()
        service_running_tasks = list(
            filter(
                lambda tsk: tsk.get('Status').get('State') == 'running',
                service_tasks
            )
        )
        return dict(
            name=svc_attrs.get('Name'),
            status='{0}/{1}'.format(
                len(service_running_tasks),
                svc_attrs.get('Mode').get('Replicated').get('Replicas')
            )
        )
