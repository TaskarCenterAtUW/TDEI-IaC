import json
import os
from azure.mgmt.containerinstance import ContainerInstanceManagementClient

class ContainerInstaces:
    def __init__(self, credential, subscription_id, resource_group):
        self.client = ContainerInstanceManagementClient(
            credential, subscription_id)
        self.resource_group = resource_group

    
    def provision(self, config_name, environment, location):

        # Load postgresql config file.
        current_dir = os.path.dirname(__file__)
        config_file = os.path.join(
            current_dir, "config", config_name, "config.json")
        
        containers_config_file = open(config_file)
        containers_config = json.load(containers_config_file)
        print(f"Loaded postgresql config file {config_file}")