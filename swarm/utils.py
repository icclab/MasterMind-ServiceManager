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

import re

from typing import Union, Text

RE_CONVERT_TIME = r'^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+|\d+\.\d+)s)' \
                  r'?(?:(\d+)ms)?(?:(\d+)us)?$'
regexp_time = re.compile(RE_CONVERT_TIME, re.ASCII | re.IGNORECASE)

SECS_TO_NANOSECS = 1000000000


def convert_time_string_to_secs(string: str) -> int:
    match = regexp_time.match(string)
    if not match:
        raise ValueError("String {0} has an invalid representation")
    h, m, s, ms, us = match.groups()
    h = int(h) if h else 0
    m = int(m) if m else 0
    s = int(float(s)) if s else 0
    total_time_seconds = h*3600 + m*60 + s
    return total_time_seconds


def convert_time_to_secs(pr: Union[Text, int]) -> int:
    if isinstance(pr, Text):
        return convert_time_string_to_secs(pr)
    elif isinstance(pr, int):
        return pr


def convert_time_to_nano_secs(pr: Union[Text, int]) -> int:
    secs = convert_time_to_secs(pr)
    if secs:
        return secs * SECS_TO_NANOSECS
