"""
This type stub file was generated by pyright.
"""

from hvac.api.vault_api_base import VaultApiBase

"""USERPASS methods module."""
DEFAULT_MOUNT_POINT = ...
class Userpass(VaultApiBase):
    """USERPASS Auth Method (API).
    Reference: https://www.vaultproject.io/api/auth/userpass/index.html
    """
    def create_or_update_user(self, username, password=..., policies=..., mount_point=..., **kwargs):
        """
        Create/update user in userpass.

        Supported methods:
            POST: /auth/{mount_point}/users/{username}. Produces: 204 (empty body)

        :param username: The username for the user.
        :type username: str | unicode
        :param password: The password for the user. Only required when creating the user.
        :type password: str | unicode
        :param policies: The list of policies to be set on username created.
        :type policies: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :param kwargs: Additional arguments to pass along with the corresponding request to Vault.
        :type kwargs: dict
        """
        ...
    
    def list_user(self, mount_point=...):
        """
        List existing users that have been created in the auth method

        Supported methods:
            LIST: /auth/{mount_point}/users. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the list_groups request.
        :rtype: dict
        """
        ...
    
    def read_user(self, username, mount_point=...):
        """
        Read user in the auth method.

        Supported methods:
            GET: /auth/{mount_point}/users/{username}. Produces: 200 application/json

        :param username: The username for the user.
        :type name: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the read_group request.
        :rtype: dict
        """
        ...
    
    def delete_user(self, username, mount_point=...):
        """
        Delete user in the auth method.

        Supported methods:
            GET: /auth/{mount_point}/users/{username}. Produces: 200 application/json

        :param username: The username for the user.
        :type name: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the read_group request.
        :rtype: dict
        """
        ...
    
    def update_password_on_user(self, username, password, mount_point=...):
        """
        update password for the user in userpass.

        Supported methods:
            POST: /auth/{mount_point}/users/{username}/password. Produces: 204 (empty body)

        :param username: The username for the user.
        :type username: str | unicode
        :param password: The password for the user. Only required when creating the user.
        :type password: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        """
        ...
    
    def login(self, username, password, use_token=..., mount_point=...):
        """
        Log in with USERPASS credentials.

        Supported methods:
            POST: /auth/{mount_point}/login/{username}. Produces: 200 application/json

        :param username: The username for the user.
        :type username: str | unicode
        :param password: The password for the user. Only required when creating the user.
        :type password: str | unicode
        :param mount_point: The "path" the method/backend was mounted on.
        :type mount_point: str | unicode
        """
        ...
    

