# swagger_client.VolumeApi

All URIs are relative to *http://127.0.0.1:8080/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_volume**](VolumeApi.md#create_volume) | **POST** /volume | Create a volume with the given name
[**delete_volume**](VolumeApi.md#delete_volume) | **DELETE** /volume/delete | Remove volume with given name
[**get_volumes**](VolumeApi.md#get_volumes) | **GET** /volume | Obtain a list of defined volumes


# **create_volume**
> create_volume(volume)

Create a volume with the given name



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.VolumeApi()
volume = swagger_client.Volume() # Volume | Definition of volume to be created

try:
    # Create a volume with the given name
    api_instance.create_volume(volume)
except ApiException as e:
    print("Exception when calling VolumeApi->create_volume: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **volume** | [**Volume**](Volume.md)| Definition of volume to be created | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_volume**
> delete_volume(volume)

Remove volume with given name



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.VolumeApi()
volume = swagger_client.Volume() # Volume | Volume to be removed

try:
    # Remove volume with given name
    api_instance.delete_volume(volume)
except ApiException as e:
    print("Exception when calling VolumeApi->delete_volume: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **volume** | [**Volume**](Volume.md)| Volume to be removed | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_volumes**
> get_volumes(swarm)

Obtain a list of defined volumes



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.VolumeApi()
swarm = swagger_client.Swarm() # Swarm | Swarm which is being queried for volumes

try:
    # Obtain a list of defined volumes
    api_instance.get_volumes(swarm)
except ApiException as e:
    print("Exception when calling VolumeApi->get_volumes: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **swarm** | [**Swarm**](Swarm.md)| Swarm which is being queried for volumes | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

