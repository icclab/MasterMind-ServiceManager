# swagger-client
No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

This Python package is automatically generated by the [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) project:

- API version: 1.0.0
- Package version: 1.0.0
- Build package: io.swagger.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import swagger_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import swagger_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NetworkApi(swagger_client.ApiClient(configuration))
network = swagger_client.Network() # Network | Definition of network to be created

try:
    # Create a network with the given name
    api_instance.create_network(network)
except ApiException as e:
    print("Exception when calling NetworkApi->create_network: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://127.0.0.1:8080/v1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*NetworkApi* | [**create_network**](docs/NetworkApi.md#create_network) | **POST** /network | Create a network with the given name
*NetworkApi* | [**delete_network**](docs/NetworkApi.md#delete_network) | **DELETE** /network/delete | Remove network with given name
*NetworkApi* | [**get_networks**](docs/NetworkApi.md#get_networks) | **GET** /network | Obtain a list of defined networks
*StackApi* | [**delete_stack**](docs/StackApi.md#delete_stack) | **POST** /stack/delete/{name} | Delete services of a stack
*StackApi* | [**deploy_stack**](docs/StackApi.md#deploy_stack) | **POST** /stack | Deploy a new stack
*StackApi* | [**get_stack**](docs/StackApi.md#get_stack) | **POST** /stack/{name} | Get the list of services of a stack
*SwarmApi* | [**swarm_status**](docs/SwarmApi.md#swarm_status) | **POST** /swarm | Get swarm status


## Documentation For Models

 - [Network](docs/Network.md)
 - [Stack](docs/Stack.md)
 - [Swarm](docs/Swarm.md)


## Documentation For Authorization

 All endpoints do not require authorization.


## Author

gaea@zhaw.ch
