import json
import os
from azure.mgmt.network import NetworkManagementClient
from infra.keyvault.keyvault import KeyVault

class VirtualNetworks:
    def __init__(self, credential, subscription_id, resource_group):
        self.network_client = NetworkManagementClient(
            credential,subscription_id)
        self.resource_group = resource_group

    def provision(self, config_name, location, environment):
        # Load configuration files
        current_dir = os.path.dirname(__file__)
        config_file = os.path.join(current_dir, "config", config_name, "config.json")
        config_file = open(config_file)
        config = json.load(config_file)
        print(f"Loaded config file {config_file}")

        # Set the Virtual Network Name and its address space and
        vnet_name = "TDEI-" + environment + "-VNET"
        response = self.network_client.virtual_networks.begin_create_or_update(
            resource_group_name=self.resource_group,
            virtual_network_name=vnet_name,
            parameters={
                "location": location,
                "properties": config['properties']
            },
        ).result()

        KeyVault.setSecret('virtual-network', response.id)
