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
            stack_name=None,
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
        self.stack_name = stack_name
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
