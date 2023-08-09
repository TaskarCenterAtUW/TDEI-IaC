import subprocess
import json
from azure.keyvault.secrets import SecretClient
import re
import os

class KeyVault(object):
    attributes = None

    @classmethod
    def initialize(cls, credential, resource_group, environment):
        cls.resource_group = resource_group
        cls.key_vault_name = 'tdei-' + environment

        # Check if vault already exists
        command = 'az keyvault show --name ' + cls.key_vault_name
        return_code, result = cls.__execute_command(cls, command)
        if return_code == 0:
            print(f"Loaded KeyVault: {cls.key_vault_name}")
            cls.attributes = result
        else:
            # Create keyvault if it does not exist
            print(f"Provisioned KeyVault: {cls.key_vault_name}")
            command = 'az keyvault create --name ' + cls.key_vault_name + \
                ' --resource-group ' + cls.resource_group
            return_code, result = cls.__execute_command(cls, command)
            if return_code == 0:
                cls.attributes = result
            else:
                print('Failed to create keyvault')
        cls._client = SecretClient(
            vault_url=cls.attributes['properties']['vaultUri'], credential=credential)

    # Execute aws cli commands via subprocess
    def __execute_command(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        response = process.communicate()
        json_message = response[0].decode()
        return (process.returncode, '' if json_message == '' else json.loads(json_message))

    # Method to set secret value in KeyVault
    @classmethod
    def setSecret(cls, key, value):
        cls._client.set_secret(key, value)

    # Method to get secret value in KeyVault
    @classmethod
    def getSecret(cls, key):
        return cls._client.get_secret(key)
    
    @classmethod
    def substitue_expression(cls, config):
        for key in config:
            # Extract all variables between braces
            variables = re.findall(r'\{.*?\}', str(config[key]))
            for variable in variables:
                # Extract variable name from braces
                key_vault_key = variable[1:-1].strip()
                try:
                    key_vault_value = config[key]
                    config[key] = key_vault_value.replace("{"+key_vault_key+"}", cls.getSecret(key_vault_key).value)
                except Exception as e:
                    print (f"Failed to fetch keyvault key {key_vault_key}")
                    print (e)
                    return(1)

    @classmethod
    def store_secrets(cls, config_name):
        # Load microservices config.json
        current_dir = os.path.dirname(__file__)
        config_file = os.path.join(
            current_dir, "config", config_name, "secrets.json")
        secrets_config_file = open(config_file)
        secrets = json.load(secrets_config_file)
        print(f"Loaded microservices config file {config_file}")
        for key in secrets:
            cls.setSecret(key, secrets[key])