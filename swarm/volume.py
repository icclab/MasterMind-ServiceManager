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


def get_volumes(docker_client: DockerClient) -> (BaseException, List):
    '''
    First incarnation of this just returns the list of networks
    defined on the swarm master.
    '''

    try:
        volumes = docker_client.volumes.list()
        return_val = []
        for v in volumes:
            return_val.append({'name': v.name, 'id': v.id})
        return None, return_val
    except docker.errors.APIError as err:
        logger.info(
            "Error obtaining list of networks from swarm - error message: {1}"
            .format(err))
        return err, None


def create_volume(docker_client: DockerClient, name: str) -> (bool, Exception):
    '''
    Create a network based on basic inputs provided.
    '''
    v = Volume(name)

    # return_val is True or False
    return_val = v.create(docker_client)

    return return_val, None


# def delete_network(docker_client: DockerClient, name: str) -> (bool, Exception):
#     '''Remove a network from the Swarm.
#     '''

#     err, networks = get_networks(docker_client)

#     print('Networks = {0}'.format(str(networks)))

#     if err is None:
#         # look for the network in the list
#         found = False
#         for n in networks:
#             print('looking for {0} - current network {1}'.format(name, n['name']))
#             if n['name'] == name:
#                 # remove this network
#                 net = docker_client.networks.get(n['id'])
#                 net.remove()
#                 found = True

#     return found, err

#     # def get_node_list_by_role(role: str):
#     #     return docker_client.nodes.list(filters={'role': role})

#     # manager_list = list(
#     #     map(_filter_node_info, get_node_list_by_role('manager'))
#     # )
#     # worker_list = list(
#     #     map(_filter_node_info, get_node_list_by_role('worker'))
#     # )
#     # return {'managers': manager_list, 'workers': worker_list}

