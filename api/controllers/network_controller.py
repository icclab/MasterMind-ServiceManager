import connexion
from api.models.network import Network
from api.models.swarm import Swarm
from api.controllers.stack_controller import get_client, create_temp_files, \
    response, close_temp_files
# from swarm.swarm import get_swarm_status
from swarm.network import get_networks as get_swarm_networks
from swarm.network import create_network as create_swarm_network
from swarm.network import delete_network as delete_swarm_network
import json
from docker.errors import APIError
from requests.exceptions import ConnectionError


def get_networks_1(swarm):
    """
    GET /v1/network/
    """

    return get_networks(swarm)


def get_networks(swarm):
    """
    GET /v1/network/
    """

    if connexion.request.is_json:
        swarm = Swarm.from_dict(connexion.request.get_json())
    temp_files = dict()

    try:
        temp_files = create_temp_files(swarm.ca_cert,
                                       swarm.cert,
                                       swarm.cert_key)
        cli = get_client(swarm.engine_url, tls=temp_files)

        # srm_status = get_swarm_status(cli)
        networks = get_swarm_networks(cli)

    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the Docker engine is reachable.")
    except APIError:
        return response(409, "Error creating network on Swarm")

    finally:
        if temp_files:
            close_temp_files(temp_files)
    return response(200, "", json.dumps(networks))


def create_network_1(network):
    return create_network(network)


def create_network(network):
    """
    POST /v1/network/
    """

    # print(str(network))
    if connexion.request.is_json:
        # swarm = Swarm.from_dict(connexion.request.get_json())
        swarm = Swarm(engine_url=network['engine-url'], ca_cert=network['ca-cert'], cert=network['cert'], cert_key=network['cert-key']) 
    # temp_files = dict()

    temp_files = create_temp_files(swarm.ca_cert,
                                   swarm.cert,
                                   swarm.cert_key)
    cli = get_client(swarm.engine_url, tls=temp_files)

    # TODO - add error checking here.
    created, exception = create_swarm_network(cli, network['name'])

    response_code = 201
    response_message = "Network created."

    if created == False:
        print(type(exception))
        if type(exception) == ConnectionError:
            response_code = 503
            response_message = "Connection error - please check if the Docker engine is reachable."
        if type(exception) == APIError:
            response_code = 409
            response_message = "Error creating network on Swarm."

    if temp_files:
        close_temp_files(temp_files)
    
    return response(response_code, response_message)


def delete_network(network):
    
    """
    DELETE /v1/network/delete/
    """

    print('in delete_network...')

    if connexion.request.is_json:
        # swarm = Swarm.from_dict(connexion.request.get_json())
        swarm = Swarm(engine_url=network['engine-url'], ca_cert=network['ca-cert'], cert=network['cert'], cert_key=network['cert-key']) 
    # temp_files = dict()

    temp_files = create_temp_files(swarm.ca_cert,
                                   swarm.cert,
                                   swarm.cert_key)
    cli = get_client(swarm.engine_url, tls=temp_files)

    # TODO - add error checking here.
    deleted, exception = delete_swarm_network(cli, network['name'])

    response_code = 200
    response_message = "Network deleted."

    if deleted == False:
        print(type(exception))
        if type(exception) == ConnectionError:
            response_code = 503
            response_message = "Connection error - please check if the Docker engine is reachable."
        if type(exception) == APIError:
            response_code = 409
            response_message = "Error creating network on Swarm."

    if temp_files:
        close_temp_files(temp_files)
    
    return response(response_code, response_message)


# def swarm_status(swarm):
#     """
#     POST /v1/swarm/
#     """
#     if connexion.request.is_json:
#         swarm = Swarm.from_dict(connexion.request.get_json())
#     temp_files = dict()

#     try:
#         temp_files = create_temp_files(swarm.ca_cert,
#                                        swarm.cert,
#                                        swarm.cert_key)
#         cli = get_client(swarm.engine_url, tls=temp_files)

#         srm_status = get_swarm_status(cli)
#     except ConnectionError:
#         return response(400, "Connection error, "
#                              "please check if the Docker engine is
#                               reachable.")
#     finally:
#         if temp_files:
#             close_temp_files(temp_files)
#     return response(200, "", {"swarm_status": str(srm_status)})
