"""
This type stub file was generated by pyright.
"""

from abc import ABCMeta, abstractmethod
from hvac.api.vault_api_base import VaultApiBase

"""Base class used by all hvac api "category" classes."""
logger = ...
class VaultApiCategory(VaultApiBase, metaclass=ABCMeta):
    """Base class for API categories."""
    def __init__(self, adapter) -> None:
        """API Category class constructor.

        :param adapter: Instance of :py:class:`hvac.adapters.Adapter`; used for performing HTTP requests.
        :type adapter: hvac.adapters.Adapter
        """
        ...
    
    def __getattr__(self, item): # -> Any:
        """Get an instance of an class instance in this category where available.

        :param item: Name of the class being requested.
        :type item: str | unicode
        :return: The requested class instance where available.
        :rtype: hvac.api.VaultApiBase
        """
        ...
    
    @property
    def adapter(self): # -> Unknown:
        """Retrieve the adapter instance under the "_adapter" property in use by this class.

        :return: The adapter instance in use by this class.
        :rtype: hvac.adapters.Adapter
        """
        ...
    
    @adapter.setter
    def adapter(self, adapter): # -> None:
        """Sets the adapter instance under the "_adapter" property in use by this class.

        Also sets the adapter property for all implemented classes under this category.

        :param adapter: New adapter instance to set for this class and all implemented classes under this category.
        :type adapter: hvac.adapters.Adapter
        """
        ...
    
    @property
    @abstractmethod
    def implemented_classes(self):
        """List of implemented classes under this category.

        :return: List of implemented classes under this category.
        :rtype: List[hvac.api.VaultApiBase]
        """
        ...
    
    @property
    def unimplemented_classes(self):
        """List of known unimplemented classes under this category.

        :return: List of known unimplemented classes under this category.
        :rtype: List[str]
        """
        ...
    
    @staticmethod
    def get_private_attr_name(class_name): # -> str:
        """Helper method to prepend a leading underscore to a provided class name.

        :param class_name: Name of a class under this category.
        :type class_name: str|unicode
        :return: The private attribute label for the provided class.
        :rtype: str
        """
        ...
    


