# coding: utf-8

"""
    MasterMind Service Manager

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: gaea@zhaw.ch
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class Network(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'engine_url': 'str',
        'ca_cert': 'str',
        'cert': 'str',
        'cert_key': 'str',
        'name': 'str'
    }

    attribute_map = {
        'engine_url': 'engine-url',
        'ca_cert': 'ca-cert',
        'cert': 'cert',
        'cert_key': 'cert-key',
        'name': 'name'
    }

    def __init__(self, engine_url=None, ca_cert=None, cert=None, cert_key=None, name=None):  # noqa: E501
        """Network - a model defined in Swagger"""  # noqa: E501

        self._engine_url = None
        self._ca_cert = None
        self._cert = None
        self._cert_key = None
        self._name = None
        self.discriminator = None

        self.engine_url = engine_url
        if ca_cert is not None:
            self.ca_cert = ca_cert
        if cert is not None:
            self.cert = cert
        if cert_key is not None:
            self.cert_key = cert_key
        self.name = name

    @property
    def engine_url(self):
        """Gets the engine_url of this Network.  # noqa: E501


        :return: The engine_url of this Network.  # noqa: E501
        :rtype: str
        """
        return self._engine_url

    @engine_url.setter
    def engine_url(self, engine_url):
        """Sets the engine_url of this Network.


        :param engine_url: The engine_url of this Network.  # noqa: E501
        :type: str
        """
        if engine_url is None:
            raise ValueError("Invalid value for `engine_url`, must not be `None`")  # noqa: E501

        self._engine_url = engine_url

    @property
    def ca_cert(self):
        """Gets the ca_cert of this Network.  # noqa: E501


        :return: The ca_cert of this Network.  # noqa: E501
        :rtype: str
        """
        return self._ca_cert

    @ca_cert.setter
    def ca_cert(self, ca_cert):
        """Sets the ca_cert of this Network.


        :param ca_cert: The ca_cert of this Network.  # noqa: E501
        :type: str
        """

        self._ca_cert = ca_cert

    @property
    def cert(self):
        """Gets the cert of this Network.  # noqa: E501


        :return: The cert of this Network.  # noqa: E501
        :rtype: str
        """
        return self._cert

    @cert.setter
    def cert(self, cert):
        """Sets the cert of this Network.


        :param cert: The cert of this Network.  # noqa: E501
        :type: str
        """

        self._cert = cert

    @property
    def cert_key(self):
        """Gets the cert_key of this Network.  # noqa: E501


        :return: The cert_key of this Network.  # noqa: E501
        :rtype: str
        """
        return self._cert_key

    @cert_key.setter
    def cert_key(self, cert_key):
        """Sets the cert_key of this Network.


        :param cert_key: The cert_key of this Network.  # noqa: E501
        :type: str
        """

        self._cert_key = cert_key

    @property
    def name(self):
        """Gets the name of this Network.  # noqa: E501


        :return: The name of this Network.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Network.


        :param name: The name of this Network.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Network, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Network):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
