import docker
from src.swarm.stack import (create_stack, get_stack_health, remove_stack)


def get_engine_status(engine) -> str:
    cli = get_client(engine)
    try:
        cli.ping()
    except:
        raise NotImplemented
    return ''


def delete_stack(name, delete_stack) -> str:
    cli = get_client(delete_stack)

    remove_stack(name, cli)
    return ''


def deploy_stack(stack) -> str:
    cli = get_client(stack)
    stack_name = stack['name']

    create_stack(stack_name, stack['compose-file'], cli)

    return ''


def get_stack_status(name, get_stack) -> str:
    cli = get_client(get_stack)
    get_stack_health(name, cli)
    return ''


def update_stack(stack) -> str:
    return ''


def get_client(cli):
    return docker.DockerClient(base_url=cli['engine-url'],
                               version="1.26",
                               tls=False)
