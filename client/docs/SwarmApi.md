# swagger_client.SwarmApi

All URIs are relative to *http://127.0.0.1:8080/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**swarm_status**](SwarmApi.md#swarm_status) | **POST** /swarm | Get swarm status


# **swarm_status**
> swarm_status(swarm)

Get swarm status



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SwarmApi()
swarm = swagger_client.Swarm() # Swarm | Get Swarm

try:
    # Get swarm status
    api_instance.swarm_status(swarm)
except ApiException as e:
    print("Exception when calling SwarmApi->swarm_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **swarm** | [**Swarm**](Swarm.md)| Get Swarm | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

