import keyring
from pathlib import Path
import secrets
import tomllib
from typing import Any, Dict, Optional

from infisical_sdk import InfisicalSDKClient, client


class Secrets:
    def __init__(self, config_path: Optional[str] = None):
        with open(Path(__file__).parent / 'conf' / 'config.toml', 'rb') as f1:
            self.__config =tomllib.load(f1)

        with open(Path(__file__).parent / 'conf' / 'sensitive.toml', 'rb') as f2:
            self.__sensitive =tomllib.load(f2)

        self.env = self.__config["CONFIG"].get("ENV", "NULL_DEV")
        self.base_url = self.__config["CONFIG"].get("BASE_URL", "NULL_URL")
        self.client_id = self.__sensitive["INFISICAL"].get("CLIENT_ID", "NULL_DEV")
        self.project_id = self.__sensitive["INFISICAL"].get("PRJ_ID", "NULL_PRJ")
        self.client_secret = keyring.get_password(self.base_url, self.__config["CONFIG"].get("SECRET_NAME", "NULL_SECRET"))

        # Initialize the client
        client = InfisicalSDKClient(host=self.base_url)

        # Authenticate (example using Universal Auth)
        client.auth.universal_auth.login(
            client_id=self.client_id, 
            client_secret=self.client_secret
        )

        self.client = client


    def get_all_secrets(self):
        
        # Use the SDK to interact with Infisical
        secrets = self.client.secrets.list_secrets(project_id=self.project_id, environment_slug=self.env, secret_path="/")

        # print(secrets)
        return secrets
    


    def get_secret_by_name(self, secret_name: str = None) -> Optional[Dict[str, Any]]:

        if secret_name is None:
            secret_name = self.__config["CONFIG"].get("SECRET_NAME", "NULL_SECRET")

        secret = self.client.secrets.get_secret_by_name(secret_name=secret_name, project_id=self.project_id, environment_slug=self.env, secret_path="/", expand_secret_references=False)

        return secret


if __name__ == "__main__":
    secrets = Secrets()
    secrets.get_all_secrets()

    print(secrets.get_secret_by_name().secretValue)