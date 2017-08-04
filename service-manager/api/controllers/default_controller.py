from __future__ import absolute_import
from serviceManager.manager import docker_client
from serviceManager.manager.stack.stack import (create_stack,
                                                get_stack_health,
                                                remove_stack)


def get_engine_status(engine) -> str:
    cli = get_client(engine)
    try:
        cli.ping()
    except:
        raise NotImplemented
    return ''


def delete_stack(name, deleteStack) -> str:
    cli = get_client(deleteStack)

    remove_stack(name, cli)
    return ''


def deploy_stack(stack) -> str:
    cli = get_client(stack)
    stack_name = stack['name']

    create_stack(stack_name, stack['compose-file'], cli)

    return ''


def get_stack_status(name, getStack) -> str:
    cli = get_client(getStack)
    get_stack_health(name, cli)
    return ''


def update_stack(stack) -> str:
    return ''


def get_client(cli):
    return docker_client.get_client(host=cli['engine-url'])
