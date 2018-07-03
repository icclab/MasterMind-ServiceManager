# swagger_client.StackApi

All URIs are relative to *http://127.0.0.1:8080/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_stack**](StackApi.md#delete_stack) | **POST** /stack/delete/{name} | Delete services of a stack
[**deploy_stack**](StackApi.md#deploy_stack) | **POST** /stack | Deploy a new stack
[**get_stack**](StackApi.md#get_stack) | **POST** /stack/{name} | Get the list of services of a stack


# **delete_stack**
> delete_stack(name, stack)

Delete services of a stack

Delete services of a stack

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.StackApi()
name = 'name_example' # str | 
stack = swagger_client.Stack() # Stack | 

try:
    # Delete services of a stack
    api_instance.delete_stack(name, stack)
except ApiException as e:
    print("Exception when calling StackApi->delete_stack: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 
 **stack** | [**Stack**](Stack.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deploy_stack**
> deploy_stack(stack)

Deploy a new stack



### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.StackApi()
stack = swagger_client.Stack() # Stack | Create a Stack

try:
    # Deploy a new stack
    api_instance.deploy_stack(stack)
except ApiException as e:
    print("Exception when calling StackApi->deploy_stack: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **stack** | [**Stack**](Stack.md)| Create a Stack | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_stack**
> get_stack(name, stack)

Get the list of services of a stack

Get a list of all services of a stack

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.StackApi()
name = 'name_example' # str | 
stack = swagger_client.Stack() # Stack | 

try:
    # Get the list of services of a stack
    api_instance.get_stack(name, stack)
except ApiException as e:
    print("Exception when calling StackApi->get_stack: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 
 **stack** | [**Stack**](Stack.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

