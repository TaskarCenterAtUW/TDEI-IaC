import json
import os
from azure.mgmt.rdbms.postgresql_flexibleservers import PostgreSQLManagementClient
from azure.mgmt.rdbms.postgresql_flexibleservers.models import Server, Sku, Storage, Database
from infra.keyvault.keyvault import KeyVault

class PostgreSQLService:
    def __init__(self, credential, subscription_id, resource_group):
        self.postgres_client = PostgreSQLManagementClient(
            credential, subscription_id)
        self.resource_group = resource_group

    def provision(self, config_name, environment, location):

        # Load postgresql config file.
        current_dir = os.path.dirname(__file__)
        config_file = os.path.join(
            current_dir, "config", config_name, "postgresql.config.json")
        postgresql_config_file = open(config_file)
        postgresql_config = json.load(postgresql_config_file)
        print(f"Loaded postgresql config file {config_file}")

        # Set the postgresql instance name
        server_name = postgresql_config['server_name'] + '-' + environment
        print (f"Postgresql Instance Name: {server_name}")

        # Load postgresql secrets
        KeyVault.substitue_expression(postgresql_config['secrets'])

        # Create PostgreSQL Flexible Server.
        server_params = Server(
            sku=Sku(name=postgresql_config['sku']['name'],
                    tier=postgresql_config['sku']['tier']),
            administrator_login=postgresql_config['secrets']['administrator_login'],
            administrator_login_password=postgresql_config['secrets']['administrator_login_password'],
            storage=Storage(storage_size_gb=postgresql_config['size']),
            version=postgresql_config['version'],
            create_mode=postgresql_config['create_mode'],
            location=location
        )

        # Provision PostgreSQL Flexible instance
        print(f"Provisioning PostgreSQL Flexible Instance: {server_name}")
        postgresql_result = self.postgres_client.servers.begin_create(
            self.resource_group,
            server_name,
            server_params,
            
        ).result()
        KeyVault.setSecret(postgresql_config['server_name'] + '-hostname', postgresql_result.fully_qualified_domain_name)
        print(
            f"Completed - '{postgresql_result.fully_qualified_domain_name}'")

        # TODO: Allow public access from any Azure service within Azure to this server
        # TODO: Add extension POSTGIS to the database server

        # Provision Databases
        database_parameters = Database(
            charset="UTF8",
            collation="en_US.utf8"
        )
        for database in postgresql_config['database']:
            database_result = self.postgres_client.databases.begin_create(
                self.resource_group,
                server_name,
                database,
                parameters=database_parameters)

            print(f"Database '{database}' created successfully.")