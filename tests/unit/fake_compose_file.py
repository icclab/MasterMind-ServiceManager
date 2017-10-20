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

import yaml


def string_to_dict(string):
    return yaml.safe_load(string)


COMPOSE_WITHOUT_NETWORK_AND_VOLUMES = string_to_dict("""
version: '3'
services:
  test:
    image: test:1.13
    ports:
      - 8080:8080
    environment:
      LABEL: Test
""")

COMPOSE_WITH_NETWORK_AND_VOLUMES = string_to_dict("""
version: '3'
services:
  test:
    image: test:1.13
    networks:
      - backend
networks:
    backend:
        driver: overlay
volumes:
    test-volume:
""")
