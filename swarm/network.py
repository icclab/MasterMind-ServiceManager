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

from typing import List

logger = logging.getLogger(__name__)


class Network(object):
    def __init__(
            self,
            name,
            stack_name=None,
            driver=None,
            external=False,
            check_duplicate=True,
            driver_opts=None,
            ipam=None,
            internal=False,
            labels=None,
            enable_ipv6=False,
            **options
    ):
        self.name = name
        self.stack_name = stack_name
        self.driver = driver
        self.external = external
        self.driver_options = driver_opts
        self.ipam = ipam
        self.check_duplicate = check_duplicate
        self.internal = internal
        self.labels = labels or {}
        self.enable_ipv6 = enable_ipv6
        self.options = options

        self._initialize_network()

    def __repr__(self):
        return "<Network: {}>".format(self.name)

    def create(self, client: DockerClient)-> (bool, Exception):
        try:
            client.networks.create(name=self.name,
                                   driver=self.driver,
                                   options=self.driver_options,
                                   ipam=self.ipam,
                                   check_duplicate=self.check_duplicate,
                                   internal=self.internal,
                                   labels=self.labels)
            return True, None
        except Exception as err:
            logger.info("Error creating network {0} - error message: {1}"
                        .format(self.name, err))
            return False, err

    def remove(self, client: DockerClient) -> (bool, Exception):
        try:
            n = client.networks.list(names=self.name)
            print("Networks Found: {0}".format(n))
            n[0].remove()
            return True, None
        except Exception as err:
            return False, err

    def _initialize_network(self):
        self._network_labels()

        if self.stack_name:
            if not self.external:
                self.name = '{0}_{1}'.format(self.stack_name, self.name)
            self.labels.update({'com.docker.stack.namespace': self.stack_name})
        if self.driver_options:
            opts = self.driver_options.copy()
            for key, value in opts.items():
                self.driver_options[key] = str(value)

    def _network_labels(self):
        """
        Checks if the labels parameter is either a dict or a list of strings.
        If it is a dictionary it will just update self.container_labels,
        else it will convert the list of strings to a dictionary.
        """
        if isinstance(self.labels, list):
            def label_to_dict(label: str):
                if "=" in label:
                    label_key, label_value = label.split('=')
                    return {label_key: label_value}
                else:
                    return {label: ''}
            label_dict = dict()
            lbs = list(map(lambda lbl: label_to_dict(lbl), self.labels))
            for lb in lbs:
                label_dict.update(lb)
            self.labels = label_dict


def get_networks(docker_client: DockerClient) -> (BaseException, List):
    '''
    First incarnation of this just returns the list of networks
    defined on the swarm master.
    '''

    try:
        networks = docker_client.networks.list()
        return_val = []
        for n in networks:
            return_val.append({'name': n.name, 'id': n.id})
        return None, return_val
    except docker.errors.APIError as err:
        logger.info(
            "Error obtaining list of networks from swarm - error message: {1}"
            .format(err))
        return err, None


def create_network(docker_client: DockerClient, name: str) -> bool:
    '''
    Create a network based on basic inputs provided.
    '''
    n = Network(name)

    # return_val is True or False
    return_val = n.create(docker_client)

    return return_val


def delete_network(docker_client: DockerClient, name: str) -> (bool, Exception):
    '''Remove a network from the Swarm.
    '''

    err, networks = get_networks(docker_client)

    print('Networks = {0}'.format(str(networks)))

    if err is None:
        # look for the network in the list
        found = False
        for n in networks:
            print('looking for {0} - current network {1}'.format(name, n['name']))
            if n['name'] == name:
                # remove this network
                net = docker_client.networks.get(n['id'])
                net.remove()
                found = True

    return found, err

    # def get_node_list_by_role(role: str):
    #     return docker_client.nodes.list(filters={'role': role})

    # manager_list = list(
    #     map(_filter_node_info, get_node_list_by_role('manager'))
    # )
    # worker_list = list(
    #     map(_filter_node_info, get_node_list_by_role('worker'))
    # )
    # return {'managers': manager_list, 'workers': worker_list}
