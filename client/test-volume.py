#! /usr/bin/env python

from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from swagger_client.configuration import Configuration
from pprint import pprint

def read_file(filename: str) -> str:
	'''Reads the given file into a string and returns this as a string.
	'''

	f = open(filename,"r")
	string = f.read()
	f.close()

	return string


configuration = swagger_client.Configuration()
configuration.host = 'http://127.0.0.1:8081/v1'

# engine_url='tcp://160.85.2.17:2376'
engine_url='tcp://160.85.2.17:2376'
ca_cert_file='../../client/secure-docker-socket/ca.pem'
cert_file='../../client/secure-docker-socket/cert.pem'
cert_key_file='../../client/secure-docker-socket/key.pem'
volume_name ='network_name2'

ca_cert = read_file(ca_cert_file)
cert = read_file(cert_file)
cert_key = read_file(cert_key_file)

# create an instance of the API class
api_instance = swagger_client.VolumeApi(swagger_client.ApiClient(configuration))
volume = swagger_client.Volume(engine_url=engine_url, ca_cert=ca_cert, cert=cert, cert_key=cert_key, name=volume_name) # Network | Definition of network to be created

try:
    # Create a network with the given name
    api_instance.create_volume(volume)
    print('Test volume creation finished...')

    api_instance.delete_volume(volume)
    print('Test volume deletion finished...')

except ApiException as e:
    print("Exception when calling NetworkApi->create_network: %s\n" % e)
