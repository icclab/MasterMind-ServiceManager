from pprint import pformat
from typing import TypeVar, Type
from six import iteritems
from ..util import deserialize_model

T = TypeVar('T')


class Model(object):
    # swaggerTypes: The key is attribute name and the value is attribute type.
    swagger_types = {}

    # attributeMap: The key is attribute name and the value is json key
    # in definition.
    attribute_map = {}
    _engine_url = None
    _ca_cert = None
    _cert = None
    _cert_key = None

    @classmethod
    def from_dict(cls: Type[T], dikt) -> T:
        """
        Returns the dict as a model
        """
        return deserialize_model(dikt, cls)

    def to_dict(self):
        """
        Returns the model properties as a dict

        :rtype: dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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

        return result

    def to_str(self):
        """
        Returns the string representation of the model

        :rtype: str
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

    @property
    def engine_url(self) -> str:
        """
        Gets the engine_url of this Stack.

        :return: The engine_url of this Stack.
        :rtype: str
        """
        return self._engine_url

    @engine_url.setter
    def engine_url(self, engine_url: str):
        """
        Sets the engine_url of this Stack.

        :param engine_url: The engine_url of this Stack.
        :type engine_url: str
        """
        if engine_url is None:
            raise ValueError(
                "Invalid value for `engine_url`, must not be `None`")

        self._engine_url = engine_url

    @property
    def ca_cert(self) -> str:
        """
        Gets the ca_cert of this Stack.

        :return: The ca_cert of this Stack.
        :rtype: str
        """
        return self._ca_cert

    @ca_cert.setter
    def ca_cert(self, ca_cert: str):
        """
        Sets the ca_cert of this Stack.

        :param ca_cert: The ca_cert of this Stack.
        :type ca_cert: str
        """

        self._ca_cert = ca_cert

    @property
    def cert(self) -> str:
        """
        Gets the cert of this Stack.

        :return: The cert of this Stack.
        :rtype: str
        """
        return self._cert

    @cert.setter
    def cert(self, cert: str):
        """
        Sets the cert of this Stack.

        :param cert: The cert of this Stack.
        :type cert: str
        """

        self._cert = cert

    @property
    def cert_key(self) -> str:
        """
        Gets the cert_key of this Stack.

        :return: The cert_key of this Stack.
        :rtype: str
        """
        return self._cert_key

    @cert_key.setter
    def cert_key(self, cert_key: str):
        """
        Sets the cert_key of this Stack.

        :param cert_key: The cert_key of this Stack.
        :type cert_key: str
        """

        self._cert_key = cert_key
