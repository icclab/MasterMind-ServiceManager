# swagger_client.NetworkApi

All URIs are relative to *http://127.0.0.1:8080/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_network**](NetworkApi.md#create_network) | **POST** /network | Create a network with the given name
[**create_network_0**](NetworkApi.md#create_network_0) | **POST** /create_network | Create a network with a given name
[**delete_network**](NetworkApi.md#delete_network) | **DELETE** /network/delete | Remove network with given name
[**get_networks**](NetworkApi.md#get_networks) | **GET** /network | Obtain a list of defined networks
[**get_networks_0**](NetworkApi.md#get_networks_0) | **POST** /get_networks | Get a list of networks from a swarm


# **create_network**
> create_network(network)

Create a network with the given name



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NetworkApi()
network = swagger_client.Network() # Network | Definition of network to be created

try:
    # Create a network with the given name
    api_instance.create_network(network)
except ApiException as e:
    print("Exception when calling NetworkApi->create_network: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **network** | [**Network**](Network.md)| Definition of network to be created | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_network_0**
> create_network_0(swarm, network)

Create a network with a given name



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NetworkApi()
swarm = swagger_client.Swarm() # Swarm | Swarm on which network will be created
network = swagger_client.Network() # Network | Network to be created

try:
    # Create a network with a given name
    api_instance.create_network_0(swarm, network)
except ApiException as e:
    print("Exception when calling NetworkApi->create_network_0: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **swarm** | [**Swarm**](Swarm.md)| Swarm on which network will be created | 
 **network** | [**Network**](Network.md)| Network to be created | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_network**
> delete_network(network)

Remove network with given name



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NetworkApi()
network = swagger_client.Network() # Network | Network to be removed

try:
    # Remove network with given name
    api_instance.delete_network(network)
except ApiException as e:
    print("Exception when calling NetworkApi->delete_network: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **network** | [**Network**](Network.md)| Network to be removed | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_networks**
> get_networks(swarm)

Obtain a list of defined networks



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NetworkApi()
swarm = swagger_client.Swarm() # Swarm | Swarm which is being queried for networks

try:
    # Obtain a list of defined networks
    api_instance.get_networks(swarm)
except ApiException as e:
    print("Exception when calling NetworkApi->get_networks: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **swarm** | [**Swarm**](Swarm.md)| Swarm which is being queried for networks | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_networks_0**
> get_networks_0(swarm)

Get a list of networks from a swarm



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.NetworkApi()
swarm = swagger_client.Swarm() # Swarm | Swarm on which network will be created

try:
    # Get a list of networks from a swarm
    api_instance.get_networks_0(swarm)
except ApiException as e:
    print("Exception when calling NetworkApi->get_networks_0: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **swarm** | [**Swarm**](Swarm.md)| Swarm on which network will be created | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

