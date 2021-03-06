# coding: utf-8

"""
    MasterMind Service Manager

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: gaea@zhaw.ch
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import swagger_client
from swagger_client.api.network_api import NetworkApi  # noqa: E501
from swagger_client.rest import ApiException


class TestNetworkApi(unittest.TestCase):
    """NetworkApi unit test stubs"""

    def setUp(self):
        self.api = swagger_client.api.network_api.NetworkApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_network(self):
        """Test case for create_network

        Create a network with the given name  # noqa: E501
        """
        pass

    def test_create_network_alternative(self):
        """Test case for create_network_alternative

        Create a network with a given name  # noqa: E501
        """
        pass

    def test_delete_network(self):
        """Test case for delete_network

        Remove network with given name  # noqa: E501
        """
        pass

    def test_get_networks(self):
        """Test case for get_networks

        Obtain a list of defined networks  # noqa: E501
        """
        pass

    def test_get_networks_alternative(self):
        """Test case for get_networks_alternative

        Get a list of networks from a swarm  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
