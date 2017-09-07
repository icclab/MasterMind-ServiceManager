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

import docker
from docker.types.services import ServiceMode, EndpointSpec
from typing import (List, Dict)


SERVICE_KEYS = [
    "args",
    "constraints",
    "container_labels",
    "environment",
    "entrypoint",
    "hostname",
    "image",
    "log_driver",
    "log_driver_options",
    "stop_grace_period",
    "user",
    "workdir"
]


class Service(object):
    def __init__(
            self,
            name,
            image=None,
            command=None,
            args=None,
            constraints=None,
            container_labels=None,
            client=None,
            endpoint_spec=None,
            env=None,
            hostname=None,
            labels=None,
            log_driver=None,
            log_driver_options=None,
            mode=None,
            mounts=None,
            networks=None,
            resources=None,
            restart_policy=None,
            secrets=None,
            stop_grace_period=None,
            update_config=None,
            user=None,
            workdir=None,
            **options
    ):
        self.args = args
        self.container_labels = container_labels
        self.client = client
        self.entrypoint = command
        self.endpoint_spec = None
        self.environment = env
        self.hostname = hostname
        self.image = image
        self.labels = labels or {}
        self.mode = mode
        self.name = name
        self.networks = networks
        self.options = options

    def __repr__(self):
        return "<Service: {}>".format(self.name)

    def create(self):
        self.client.services.create(self.image,
                                    args=self.args,
                                    command=self.entrypoint,
                                    container_labels=self.container_labels,
                                    env=self.environment,
                                    endpoint_spec=self.endpoint_spec,
                                    labels=self.labels,
                                    mode=self.mode,
                                    name=self.name,
                                    networks=self.networks)


def load_services(stack_name: str,
                  services_dict: Dict,
                  cli: docker.DockerClient) -> List[Service]:

    services = list()
    for service_name, service_attr in services_dict.items():
        service_configuration_dict = get_service_configuration(stack_name,
                                                               service_attr)
        service = Service(
            name=stack_name + "_" + service_name,
            client=cli,
            **service_configuration_dict
        )
        services.append(service)
    return services


def get_service_configuration(stack_name: str,
                              config_dict: Dict) -> Dict:

    services_attr_dict = dict()
    for key in SERVICE_KEYS:
        if key in config_dict:
            services_attr_dict[key] = config_dict[key]

    # Attributes that need special handling
    if "ports"in config_dict:
        services_attr_dict["endpoint_spec"] = get_service_endpoint_spec(
            config_dict["ports"])

    services_attr_dict["labels"] = {}

    # Associating the service to the stack
    services_attr_dict["labels"]["com.docker.stack.namespace"] = stack_name

    if "deploy" in config_dict:
        if "replicas" in config_dict["deploy"].keys():
            services_attr_dict["mode"] = get_service_mode(
                replicas=config_dict["deploy"].get("replicas"))

        if "labels" in config_dict["deploy"].keys():
            services_attr_dict["labels"] = config_dict["deploy"].get("labels")

    if "command" in config_dict:
        if isinstance(config_dict["command"], list):
            services_attr_dict["args"] = config_dict["command"]
        elif isinstance(config_dict["command"], str):
            services_attr_dict["args"] = [config_dict["command"]]
        else:
            raise TypeError

    if "networks" in config_dict:
        services_attr_dict["networks"] = [stack_name + "_" + network
                                          for network in
                                          config_dict["networks"]]

    if "labels" in config_dict:
        if isinstance(config_dict["labels"], dict):
            services_attr_dict["container_labels"] = config_dict["labels"]
        elif isinstance(config_dict["labels"], list):
            services_attr_dict["container_labels"] = \
                get_service_labels(config_dict["labels"])
    return services_attr_dict


def get_service_endpoint_spec(ports: List[str]) -> EndpointSpec:

    # This function needs more validation as there are different ways
    # to declare ports in a compose file
    # At the moment only "8000:8000" is supported
    ports_dict = dict()
    for p in ports:
        p_str = p.split(":")
        ports_dict[int(p_str[0])] = int(p_str[1])
    return EndpointSpec(ports=ports_dict)


def get_service_labels(labels: List[str]) -> Dict:
    label_dict = dict()
    for label in labels:
        try:
            label_key, label_value = label.split("=")
            label_dict[label_key] = label_value
        # In case the label doesn"t have any value a ValueError will be raised
        # this handles this exception adding the label without value
        except ValueError:
            label_dict[label] = ""
    return label_dict


def get_service_mode(mode: str="replicated",
                     replicas: int=None) -> ServiceMode:
    return ServiceMode(mode=mode, replicas=replicas)
