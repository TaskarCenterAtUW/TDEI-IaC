import json
import os
from infra.keyvault.keyvault import KeyVault
from azure.mgmt.cosmosdb import CosmosDBManagementClient

class LoggerDB:
    def __init__(self, credential, subscription_id, resource_group):
        self.Client = CosmosDBManagementClient(
            credential,subscription_id)
        self.resource_group = resource_group


    def provision(self, config_name, location, environment):
        # Load configuration files
        current_dir = os.path.dirname(__file__)
        config_file = os.path.join(current_dir, "config", config_name, "config.json")
        config_file = open(config_file)
        config = json.load(config_file)

        # Add the location information
        config['cosmosdb']['createUpdateParameters']['properties']['locations'][0]['locationName'] = location
        config['cosmosdb']['createUpdateParameters']['location'] = location

        # Account is created with env suffix
        account_name = config['cosmosdb']['accountName']+"-"+environment

        # Provision Account first
        response = self.Client.database_accounts.begin_create_or_update(
            resource_group_name=self.resource_group,
            account_name=account_name,
            create_update_parameters=config['cosmosdb']['createUpdateParameters']
        ).result()

        connection_info = self.Client.database_accounts.list_connection_strings(self.resource_group,account_name)
        for connections in connection_info.connection_strings:
            if connections.key_kind == "Primary" and connections.type == "MongoDB":
                primary_connection_string = connections.connection_string
                KeyVault.setSecret('loggerdb-connection-string', primary_connection_string)
                print(primary_connection_string)


        # Provision Database Next
        response=self.Client.mongo_db_resources.begin_create_update_mongo_db_database(
            resource_group_name=self.resource_group,
            account_name=account_name,
            database_name=config['cosmosdb']['name'],
            create_update_mongo_db_database_parameters={
                "location":location,
                "properties":{"options":{},"resource":{"id":config['cosmosdb']['name']}}
            }
        ).result()


        # Provision Collection Next
        response = self.Client.mongo_db_resources.begin_create_update_mongo_db_collection(
            resource_group_name=self.resource_group,
            account_name=account_name,
            database_name=config['cosmosdb']['name'],
            collection_name=config['cosmosdb']['collectionName'],
            create_update_mongo_db_collection_parameters={
                "location":location,
                "properties":{"resource":{"id":config['cosmosdb']['collectionName']}}
            }
        ).result()
        print("Provisioned Logger DB Collection")
