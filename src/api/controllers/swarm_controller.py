import connexion
from api.models.swarm import Swarm
from api.controllers.stack_controller import get_client, create_temp_files, \
    response, close_temp_files
from swarm.swarm import get_swarm_status


def swarm_status(swarm):
    if connexion.request.is_json:
        swarm = Swarm.from_dict(connexion.request.get_json())
    temp_files = dict()

    try:
        temp_files = create_temp_files(swarm.ca_cert,
                                       swarm.cert,
                                       swarm.cert_key)
        cli = get_client(swarm.engine_url, tls=temp_files)

        srm_status = get_swarm_status(cli)
    except ConnectionError:
        return response(400, "Connection error, "
                             "please check if the Docker engine is reachable.")
    finally:
        if temp_files:
            close_temp_files(temp_files)
    return response(200, "", {"swarm_status": str(srm_status)})
