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

from .exceptions import NetworkNotFound, VolumeNotFound
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
        self.service_dict = self.compose_file.get('services')
        self.network_dict = self.compose_file.get('networks') or {}
        self.volume_dict = self.compose_file.get('volumes') or {}

        self._create_networks()
        self._create_volumes()
        self._create_services()
        return self.services, self.networks, self.volumes

    def remove(self) -> None:
        svc_list = self._get_stack_services()
        net_list = self._get_stack_networks()

        for svc in svc_list:
            svc.remove()
        for net in net_list:
            net.remove()

    def health(self) -> List[Dict]:
        svc_list = self._get_stack_services()
        svcs = list(map(
            self._filter_service_info,
            svc_list
        ))
        return svcs

    def _create_networks(self) -> None:
        def check_if_network_is_external(dictionary: Dict):
            net_name, net_attrs = dictionary
            if not net_attrs:
                net_attrs = {}
            if not net_attrs.get('external'):
                self.stack_networks.append(net_name)
                return self._create_obj_from_dict(dictionary, Network)
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
        default_net = Network(name='default',
                              stack_name=self.stack_name,
                              driver='overlay')
        default_net.create(self.client)
        self.networks.append(default_net)

    def _create_volumes(self) -> None:
        def check_if_volume_is_external(dictionary: Dict):
            vol_name, vol_attrs = dictionary
            if not vol_attrs:
                vol_attrs = {}
            if not vol_attrs.get('external'):
                return self._create_obj_from_dict(dictionary, Volume)
            if not self.client.volumes.list(names=[vol_name]):
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
            lambda sc: self._create_obj_from_dict(sc, Service),
            self.service_dict.items()
        ))
        for svc in self.services:
            if isinstance(svc, Service):
                svc.create(self.client)

    def _check_stack_service_attributes(self) -> None:
        for svc_name, svc_attrs in self.service_dict.items():
            self._check_stack_service_networks(svc_attrs.get('networks') or [])

    def _check_stack_service_networks(self, attrs: Union[List, Dict]) -> None:
        if isinstance(attrs, list):
            nets = attrs
            for net in nets:
                if net in self.stack_networks:
                    nets[nets.index(net)] = '{0}_{1}'.format(
                        self.stack_name, net
                    )
            else:
                if not self.default_network_created:
                    self._create_default_network()
                    self.default_network_created = True

    def _create_obj_from_dict(self, dictionary: Dict,
                              obj_class) -> Union[Service, Network, Volume]:
        obj_name, obj_attrs = dictionary
        if not obj_attrs:
            obj_attrs = {}
        return obj_class(obj_name, stack_name=self.stack_name, **obj_attrs)

    def _get_stack_services(self) -> Iterable[services.Service]:
        filter_lbl = 'com.docker.stack.namespace={0}'.format(self.stack_name)
        return self.client.services.list(filters={'label': filter_lbl})

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

    def _get_stack_networks(self) -> Iterable[networks.Network]:
        filter_lbl = 'com.docker.stack.namespace={0}'.format(self.stack_name)
        return self.client.networks.list(filters={'label': filter_lbl})
