import connexion
from api.models.volume import Volume
from api.models.swarm import Swarm
from api.controllers.stack_controller import get_client, create_temp_files, \
    response, close_temp_files
# from swarm.swarm import get_swarm_status
from swarm.volume import get_volumes as get_swarm_volumes
from swarm.volume import create_volume as create_swarm_volume
from swarm.volume import remove_volume as delete_swarm_volume
import json
from docker.errors import APIError
from requests.exceptions import ConnectionError

def get_volumes(swarm):
    """
    GET /v1/volume/
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
        volumes = get_swarm_volumes(cli)

    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the Docker engine is reachable.")
    except APIError:
        return response(409, "Error creating volume on Swarm")

    finally:
        if temp_files:
            close_temp_files(temp_files)
    return response(200, "", json.dumps(volumes))


def create_volume(volume):
    """
    POST /v1/volume/
    """

    # print(str(network))
    if connexion.request.is_json:
        # swarm = Swarm.from_dict(connexion.request.get_json())
        swarm = Swarm(engine_url=volume['engine-url'], ca_cert=volume['ca-cert'], cert=volume['cert'], cert_key=volume['cert-key']) 
    # temp_files = dict()

    temp_files = create_temp_files(swarm.ca_cert,
                                   swarm.cert,
                                   swarm.cert_key)
    cli = get_client(swarm.engine_url, tls=temp_files)

    # TODO - add error checking here.
    created, exception = create_swarm_volume(cli, volume['name'])

    response_code = 201
    response_message = "Volume created."

    if created == False:
        print(type(exception))
        if type(exception) == ConnectionError:
            response_code = 503
            response_message = "Connection error - please check if the Docker engine is reachable."
        if type(exception) == APIError:
            response_code = 409
            response_message = "Error creating volume on Swarm."

    if temp_files:
        close_temp_files(temp_files)
    
    return response(response_code, response_message)


def delete_volume(volume):
    
    """
    DELETE /v1/volume/delete/
    """

    print('in delete_volume...')

    if connexion.request.is_json:
        # swarm = Swarm.from_dict(connexion.request.get_json())
        swarm = Swarm(engine_url=volume['engine-url'], ca_cert=volume['ca-cert'], cert=volume['cert'], cert_key=volume['cert-key']) 
    # temp_files = dict()

    temp_files = create_temp_files(swarm.ca_cert,
                                   swarm.cert,
                                   swarm.cert_key)
    cli = get_client(swarm.engine_url, tls=temp_files)

    # TODO - add error checking here.
    # note that the remove_volume function takes the volume name first and then the client...
    # deleted, exception = delete_swarm_volume(volume['name'], cli)
    deleted = delete_swarm_volume(volume['name'], cli)

    response_code = 200
    response_message = "Volume deleted."

    if deleted == False:
        # print(type(exception))
        # if type(exception) == ConnectionError:
        #     response_code = 503
        #     response_message = "Connection error - please check if the Docker engine is reachable."
        # if type(exception) == APIError:
        #     response_code = 409
        #     response_message = "Error creating volume on Swarm."
        response_code = 409
        response_message = "Error deleting volume on Swarm."

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
