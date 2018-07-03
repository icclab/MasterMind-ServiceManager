# coding: utf-8

"""
    MasterMind Service Manager

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: gaea@zhaw.ch
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from swagger_client.api_client import ApiClient


class StackApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def delete_stack(self, name, stack, **kwargs):  # noqa: E501
        """Delete services of a stack  # noqa: E501

        Delete services of a stack  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.delete_stack(name, stack, async=True)
        >>> result = thread.get()

        :param async bool
        :param str name:  (required)
        :param Stack stack:  (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.delete_stack_with_http_info(name, stack, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_stack_with_http_info(name, stack, **kwargs)  # noqa: E501
            return data

    def delete_stack_with_http_info(self, name, stack, **kwargs):  # noqa: E501
        """Delete services of a stack  # noqa: E501

        Delete services of a stack  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.delete_stack_with_http_info(name, stack, async=True)
        >>> result = thread.get()

        :param async bool
        :param str name:  (required)
        :param Stack stack:  (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name', 'stack']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_stack" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `delete_stack`")  # noqa: E501
        # verify the required parameter 'stack' is set
        if ('stack' not in params or
                params['stack'] is None):
            raise ValueError("Missing the required parameter `stack` when calling `delete_stack`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'stack' in params:
            body_params = params['stack']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/stack/delete/{name}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def deploy_stack(self, stack, **kwargs):  # noqa: E501
        """Deploy a new stack  # noqa: E501

          # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.deploy_stack(stack, async=True)
        >>> result = thread.get()

        :param async bool
        :param Stack stack: Create a Stack (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.deploy_stack_with_http_info(stack, **kwargs)  # noqa: E501
        else:
            (data) = self.deploy_stack_with_http_info(stack, **kwargs)  # noqa: E501
            return data

    def deploy_stack_with_http_info(self, stack, **kwargs):  # noqa: E501
        """Deploy a new stack  # noqa: E501

          # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.deploy_stack_with_http_info(stack, async=True)
        >>> result = thread.get()

        :param async bool
        :param Stack stack: Create a Stack (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['stack']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method deploy_stack" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'stack' is set
        if ('stack' not in params or
                params['stack'] is None):
            raise ValueError("Missing the required parameter `stack` when calling `deploy_stack`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'stack' in params:
            body_params = params['stack']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/stack', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_stack(self, name, stack, **kwargs):  # noqa: E501
        """Get the list of services of a stack  # noqa: E501

        Get a list of all services of a stack  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_stack(name, stack, async=True)
        >>> result = thread.get()

        :param async bool
        :param str name:  (required)
        :param Stack stack:  (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.get_stack_with_http_info(name, stack, **kwargs)  # noqa: E501
        else:
            (data) = self.get_stack_with_http_info(name, stack, **kwargs)  # noqa: E501
            return data

    def get_stack_with_http_info(self, name, stack, **kwargs):  # noqa: E501
        """Get the list of services of a stack  # noqa: E501

        Get a list of all services of a stack  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_stack_with_http_info(name, stack, async=True)
        >>> result = thread.get()

        :param async bool
        :param str name:  (required)
        :param Stack stack:  (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name', 'stack']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_stack" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if ('name' not in params or
                params['name'] is None):
            raise ValueError("Missing the required parameter `name` when calling `get_stack`")  # noqa: E501
        # verify the required parameter 'stack' is set
        if ('stack' not in params or
                params['stack'] is None):
            raise ValueError("Missing the required parameter `stack` when calling `get_stack`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'stack' in params:
            body_params = params['stack']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/stack/{name}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
