# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from models.base_model_ import Model
# from swagger_server import util
import util

class Stack(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, name: str=None, compose_file: str=None, compose_vars: str=None, engine_url: str=None, ca_cert: str=None, cert: str=None, cert_key: str=None, external_files: List[object]=None):  # noqa: E501
        """Stack - a model defined in Swagger

        :param name: The name of this Stack.  # noqa: E501
        :type name: str
        :param compose_file: The compose_file of this Stack.  # noqa: E501
        :type compose_file: str
        :param compose_vars: The compose_vars of this Stack.  # noqa: E501
        :type compose_vars: str
        :param engine_url: The engine_url of this Stack.  # noqa: E501
        :type engine_url: str
        :param ca_cert: The ca_cert of this Stack.  # noqa: E501
        :type ca_cert: str
        :param cert: The cert of this Stack.  # noqa: E501
        :type cert: str
        :param cert_key: The cert_key of this Stack.  # noqa: E501
        :type cert_key: str
        :param external_files: The external_files of this Stack.  # noqa: E501
        :type external_files: List[object]
        """
        self.swagger_types = {
            'name': str,
            'compose_file': str,
            'compose_vars': str,
            'engine_url': str,
            'ca_cert': str,
            'cert': str,
            'cert_key': str,
            'external_files': List[object]
        }

        self.attribute_map = {
            'name': 'name',
            'compose_file': 'compose-file',
            'compose_vars': 'compose-vars',
            'engine_url': 'engine-url',
            'ca_cert': 'ca-cert',
            'cert': 'cert',
            'cert_key': 'cert-key',
            'external_files': 'external_files'
        }

        self._name = name
        self._compose_file = compose_file
        self._compose_vars = compose_vars
        self._engine_url = engine_url
        self._ca_cert = ca_cert
        self._cert = cert
        self._cert_key = cert_key
        self._external_files = external_files

    @classmethod
    def from_dict(cls, dikt) -> 'Stack':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Stack of this Stack.  # noqa: E501
        :rtype: Stack
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Stack.


        :return: The name of this Stack.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Stack.


        :param name: The name of this Stack.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def compose_file(self) -> str:
        """Gets the compose_file of this Stack.


        :return: The compose_file of this Stack.
        :rtype: str
        """
        return self._compose_file

    @compose_file.setter
    def compose_file(self, compose_file: str):
        """Sets the compose_file of this Stack.


        :param compose_file: The compose_file of this Stack.
        :type compose_file: str
        """

        self._compose_file = compose_file

    @property
    def compose_vars(self) -> str:
        """Gets the compose_vars of this Stack.


        :return: The compose_vars of this Stack.
        :rtype: str
        """
        return self._compose_vars

    @compose_vars.setter
    def compose_vars(self, compose_vars: str):
        """Sets the compose_vars of this Stack.


        :param compose_vars: The compose_vars of this Stack.
        :type compose_vars: str
        """

        self._compose_vars = compose_vars

    @property
    def engine_url(self) -> str:
        """Gets the engine_url of this Stack.


        :return: The engine_url of this Stack.
        :rtype: str
        """
        return self._engine_url

    @engine_url.setter
    def engine_url(self, engine_url: str):
        """Sets the engine_url of this Stack.


        :param engine_url: The engine_url of this Stack.
        :type engine_url: str
        """
        if engine_url is None:
            raise ValueError("Invalid value for `engine_url`, must not be `None`")  # noqa: E501

        self._engine_url = engine_url

    @property
    def ca_cert(self) -> str:
        """Gets the ca_cert of this Stack.


        :return: The ca_cert of this Stack.
        :rtype: str
        """
        return self._ca_cert

    @ca_cert.setter
    def ca_cert(self, ca_cert: str):
        """Sets the ca_cert of this Stack.


        :param ca_cert: The ca_cert of this Stack.
        :type ca_cert: str
        """

        self._ca_cert = ca_cert

    @property
    def cert(self) -> str:
        """Gets the cert of this Stack.


        :return: The cert of this Stack.
        :rtype: str
        """
        return self._cert

    @cert.setter
    def cert(self, cert: str):
        """Sets the cert of this Stack.


        :param cert: The cert of this Stack.
        :type cert: str
        """

        self._cert = cert

    @property
    def cert_key(self) -> str:
        """Gets the cert_key of this Stack.


        :return: The cert_key of this Stack.
        :rtype: str
        """
        return self._cert_key

    @cert_key.setter
    def cert_key(self, cert_key: str):
        """Sets the cert_key of this Stack.


        :param cert_key: The cert_key of this Stack.
        :type cert_key: str
        """

        self._cert_key = cert_key

    @property
    def external_files(self) -> List[object]:
        """Gets the external_files of this Stack.


        :return: The external_files of this Stack.
        :rtype: List[object]
        """
        return self._external_files

    @external_files.setter
    def external_files(self, external_files: List[object]):
        """Sets the external_files of this Stack.


        :param external_files: The external_files of this Stack.
        :type external_files: List[object]
        """

        self._external_files = external_files
