import json
import os
from azure.mgmt.containerinstance import ContainerInstanceManagementClient

from azure.mgmt.containerinstance.models import (
    Container,
    ContainerGroup,
    ContainerPort,
    EnvironmentVariable,
    ResourceRequests,
    ResourceRequirements,
    EnvironmentVariable,
    ImageRegistryCredential,
    OperatingSystemTypes
)
from infra.keyvault.keyvault import KeyVault


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
        container_groups = containers_config['container-groups']
        for cg in container_groups:
            containers = []
            container_group_name = cg['container_group_name'] + "-" + environment

            container_config = cg['containers'][0]

            requests = ResourceRequests(
                memory_in_gb=container_config['memory_in_gb'],
                cpu=container_config['cpu']
            )

            resources = ResourceRequirements(
                requests=requests
            )

            environment_variables = []

            for key, value in container_config['environment_variables'].items():
                environment_variables.append(EnvironmentVariable(name=key, value=value))

            for key, value in container_config['secrets'].items():
                environment_variables.append(EnvironmentVariable(name=key, value=KeyVault.getSecret(value).value))


            container = Container(
                name=container_config['name']+ "-" + environment,
                image=container_config['image'],
                resources=resources,
                ports=[ContainerPort(port=port) for port in container_config.get('ports', [])],
                environment_variables=environment_variables
            )

            containers.append(container)
           
            image_registry_credentials = [
                ImageRegistryCredential(
                    server=KeyVault.getSecret('docker-registry-server-url').value[8:],
                    username=KeyVault.getSecret('docker-registry-server-username').value,
                    password=KeyVault.getSecret('docker-registry-password').value
                )
            ]
             

            container_group = ContainerGroup(
                location="eastus",
                containers=containers,
                os_type=OperatingSystemTypes.linux,
                image_registry_credentials=image_registry_credentials
            )
            self.client.container_groups.begin_create_or_update(
                self.resource_group,
                container_group_name,
                container_group
            )

            print(f"Container group '{container_group_name}' created successfully with Docker credentials.")

            

