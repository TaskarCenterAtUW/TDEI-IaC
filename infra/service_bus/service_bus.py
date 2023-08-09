import json
import os
from azure.mgmt.servicebus import ServiceBusManagementClient
from azure.mgmt.servicebus.models import SBNamespace, SBSku, SBQueue
from infra.keyvault.keyvault import KeyVault

class ServiceBus:
    def __init__(self, credential, subscription_id, resource_group):
        self.servicebus_client = ServiceBusManagementClient(
            credential,subscription_id)
        self.resource_group = resource_group


    def provision(self, config_name, location, environment):
        # Load configuration files
        current_dir = os.path.dirname(__file__)
        config_file = os.path.join(current_dir, "config", config_name, "config.json")
        config_file = open(config_file)
        config = json.load(config_file)
        print(f"Loaded config file {config_file}")

        # Set the Service Bus Name and its parameters
        service_bus_name = config['service_bus']['name'] + "-" + environment
        print (f"Service Bus Namespace: {service_bus_name}")

        # Service bus namespaces are unique. So, check whether the Name space is available
        # Provision only if the namespace is available
        availability_result = self.servicebus_client.namespaces.check_name_availability(
            {"name": service_bus_name}
        )
        if not availability_result.name_available:
            print(f"Service Bus Namespace :{service_bus_name} is already in use.")
        else:
            service_bus_params = SBNamespace(
                sku=SBSku(name=config['service_bus']['sku']['name'],
                          tier=config['service_bus']['sku']['tier']),
                tags=config['tags'],
                location=location
            )

            # Provision the Service Bus NameSpace
            print(f"Provisioning Service Bus NameSpace: {service_bus_name}")
            servicebus_result = self.servicebus_client.namespaces.begin_create_or_update(
                resource_group_name=self.resource_group,
                namespace_name=service_bus_name,
                parameters=service_bus_params
            ).result()

            print(f"Completed - '{servicebus_result.name}'")

        rules = self.servicebus_client.namespaces.list_authorization_rules(self.resource_group, service_bus_name)

        # Find the primary connection string rule
        for r in rules:
            list_keys = self.servicebus_client.namespaces.list_keys(self.resource_group, service_bus_name, r.name)
            service_bus_connection_string = list_keys.primary_connection_string
            print(service_bus_connection_string)
            KeyVault.setSecret('service-bus-connection-string', service_bus_connection_string)

        # Set the Queue Name and its parameters
        queue_name = config['queue']['name']
        print (f"Queue Name: {queue_name}")

        queue_params = SBQueue(
            max_size_in_megabytes=config['queue']['max_size_in_megabytes'],
            max_delivery_count=config['queue']['max_delivery_count'],
            default_message_time_to_live=config['queue']['message_time_to_live']
        )

        # Provision the Queue
        print(f"Provisioning Queue: {queue_name}")
        queue_result = self.servicebus_client.queues.create_or_update(
            resource_group_name=self.resource_group,
            namespace_name=service_bus_name,
            queue_name=queue_name,
            parameters=queue_params
        )

        print(f"Completed - '{queue_result.name}'")

        # Provision Topics and their subscriptions
        for topic in config['topics']:

            # Provision the Topic
            print(f"Provisioning Topic: {topic['name']}")
            topic_result = self.servicebus_client.topics.create_or_update(
                resource_group_name=self.resource_group,
                namespace_name=service_bus_name,
                topic_name=topic['name'],
                parameters=topic['parameters']
                # Tried passing Params as SBTopic and it didn't work
            )

            print(f"Completed - '{topic_result.name}'")

            # Provision the Subscriptions to that topic if subscriptions exist
            if "subscriptions" in topic:
                for subscription in topic['subscriptions']:
                    print(f"Provisioning Subscription: {subscription['name']}")
                    subscription_result = self.servicebus_client.subscriptions.create_or_update(
                        resource_group_name=self.resource_group,
                        namespace_name=service_bus_name,
                        topic_name=topic['name'],
                        subscription_name=subscription['name'],
                        parameters=subscription['parameters']
                    )
                    print(f"Provisioning Subscription: {subscription['name']} complete")
