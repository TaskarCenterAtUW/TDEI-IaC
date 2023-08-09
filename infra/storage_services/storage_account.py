import json
import os
from azure.mgmt.storage import StorageManagementClient
from infra.keyvault.keyvault import KeyVault

class StorageAccount:
    def __init__(self, resource_group, subscription_id, credential):
        self.storage_client = StorageManagementClient(
            credential, subscription_id)
        self.resource_group = resource_group

    def provision(self, config_name, location, environment):
        # Load configuration files
        current_dir = os.path.dirname(__file__)
        config_file = os.path.join(
            current_dir, "config", config_name, "config.json")
        storage_config_file = open(config_file)
        storage_config = json.load(storage_config_file)
        print(f"Loaded storage config file {config_file}")

        for storage_account in storage_config:
            storage_account_name = storage_account + "" + environment
            print(f"Provisioning Storage Account: {storage_account_name}")
            # Check if the account name is available.
            availability_result = self.storage_client.storage_accounts.check_name_availability(
                {"name": storage_account_name}
            )
            if not availability_result.name_available:
                print(
                    f"Storage account :{storage_account_name} is already in use.")
            else:
                # The storage account name is available, so provision the account
                poller = self.storage_client.storage_accounts.begin_create(
                    self.resource_group, storage_account_name,
                    {
                        "location": location,
                        "kind": "StorageV2",
                        "sku": {"name": storage_config[storage_account]['sku']}
                    }
                )
                # Long-running operations return a poller object; calling poller.result()
                # waits for completion.
                account_result = poller.result()
                print(f"Provisioned storage account: {account_result.name}")

            # Create storage containers
            for container in storage_config[storage_account]['containers']:
                # Step 3: Retrieve the account's primary access key and generate a connection string.
                keys = self.storage_client.storage_accounts.list_keys(
                    self.resource_group, storage_account_name)
                print(
                    f"Primary key for storage account: {keys.keys[0].value}")
                conn_string = f"DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName={storage_account_name};AccountKey={keys.keys[0].value}"
                print(f"Storage account connection string: {conn_string}")
                KeyVault.setSecret('storage-connection-string', conn_string)
                # Step 4: Provision the blob container in the account (this call is synchronous)
                storage_container = self.storage_client.blob_containers.create(
                    self.resource_group, storage_account_name, container, {})
                # The fourth argument is a required BlobContainer object, but because we don't need any
                # special values there, so we just pass empty JSON.

                print(
                    f"Provisioned blob container: {storage_container.name}")
