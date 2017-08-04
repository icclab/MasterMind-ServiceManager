from typing import (List, Dict)
from .network import (Network, NETWORK_KEYS)


def load_networks(stack_name, network_dict, cli):
    # type: (str, Dict, docker.DockerClient) -> List[Network]
    networks = list()
    for network_name, network_attr in network_dict.items():
        network_configuration_dict = get_network_configuration(stack_name,
                                                               network_attr)
        network = Network(
            name=stack_name + "_" + network_name,
            client=cli,
            stack_name=stack_name,
            **network_configuration_dict
        )
        networks.append(network)
    return networks


def get_network_configuration(stack_name, config_dict):
    # type: (str, Dict) -> Dict
    network_attr_dict = dict()
    for key in NETWORK_KEYS:
        if key in config_dict:
            network_attr_dict[key] = config_dict[key]

    # if hasattr(config_dict, "external"):
        # check_external_network()
    network_attr_dict["labels"] = dict()
    network_attr_dict["labels"]["com.docker.stack.namespace"] = stack_name
    return network_attr_dict
