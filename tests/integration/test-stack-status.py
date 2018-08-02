#! /usr/bin/env python

from __future__ import print_function
# import time
import swagger_client
from swagger_client.rest import ApiException
# from swagger_client.configuration import Configuration
# from pprint import pprint
import time

# set up variables...a bit too global but that's ok
# for a small test file.
configuration = swagger_client.Configuration()
configuration.host = 'http://127.0.0.1:8081/v1'

# engine_url='tcp://160.85.2.17:2376'
engine_url = 'tcp://160.85.2.17:2376'
ca_cert_file = '../../client/secure-docker-socket/ca.pem'
cert_file = '../../client/secure-docker-socket/cert.pem'
cert_key_file = '../../client/secure-docker-socket/key.pem'
# compose_filename = 'quantum-leap/docker-compose.yml'
compose_filename = 'mkguid/docker-compose.yml'


def read_file(filename: str) -> str:
    '''Reads the given file into a string and returns this as a string.
    '''

    f = open(filename, "r")
    string = f.read()
    f.close()

    return string


def create_network(network_api_instance, network):
    # create an instance of the API class
    try:
        # Create a stack with the given name
        return_val = network_api_instance.create_network(network)
        print('Network created...')
        print('Return value: {0}'.format(return_val))

    except ApiException as e:
        print("Exception when calling NetworkAPI->create_network: %s\n" % e)


def create_stack(stack_api_instance, stack):
    try:
        # Create a stack with the given name
        return_val = stack_api_instance.deploy_stack(stack)
        print('Test service creation finished...')
        print('Return value: {0}'.format(return_val))

    except ApiException as e:
        print("Exception when calling StackAPI->deploy_stack: %s\n" % e)


def delete_stack(stack_api_instance, stack_name, stack):
    try:
        stack_api_instance.delete_stack(stack_name, stack)
        print('Test service deletion finished...')

    except ApiException as e:
        print("Exception when calling StackAPI->deploy_stack: %s\n" % e)


def delete_network(network_api_instance, network):
    try:
        # Create a stack with the given name
        network_api_instance.delete_network(network)
        print('Network created...')

    except ApiException as e:
        print("Exception when calling NetworkAPI->create_network: %s\n" % e)


def get_stack_status(stack_api_instance, name, stack):
    try:
        # Create a stack with the given name
        return_val = stack_api_instance.get_stack(name, stack)
        print('get_stack_status: Return value: {0}'.format(return_val))

    except ApiException as e:
        print("Exception when calling StackAPI->deploy_stack: %s\n" % e)


def main():

    ca_cert = read_file(ca_cert_file)
    cert = read_file(cert_file)
    cert_key = read_file(cert_key_file)
    compose_file = read_file(compose_filename)
    stack_name = 'test-stacker'
    network_name = 'frontend'

    network_api_instance = \
        swagger_client.NetworkApi(swagger_client.ApiClient(configuration))
    # Network | Definition of network to be created
    network = swagger_client.Network(engine_url=engine_url,
                                     ca_cert=ca_cert, cert=cert,
                                     cert_key=cert_key,
                                     name=network_name)

    # create an instance of the API class
    stack_api_instance = \
        swagger_client.StackApi(swagger_client.ApiClient(configuration))
    # stack | Definition of stack to be created
    stack = swagger_client.Stack(engine_url=engine_url,
                                 ca_cert=ca_cert, cert=cert,
                                 cert_key=cert_key,
                                 compose_file=compose_file,
                                 compose_vars="",
                                 external_files=[],
                                 name=stack_name)

    create_network(network_api_instance, network)
    create_stack(stack_api_instance, stack)
    time.sleep(45)
    get_stack_status(stack_api_instance, stack_name, stack)
    # delete_stack(stack_api_instance, stack_name, stack)
    # delete_network(network_api_instance, network)


if __name__ == '__main__':
    main()
