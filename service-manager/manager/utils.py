from __future__ import absolute_import
from typing import Dict
from yaml import safe_load


def parse_compose_file(compose):
    # type: (str) -> Dict

    compose_parsed = safe_load(compose)
    return compose_parsed

