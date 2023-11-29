import json
import os
from infra.keyvault.keyvault import KeyVault
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.models import (
    LogSettings,
    DiagnosticSettingsResource,
    RetentionPolicy
)


class DiagnosticSettings:
    def __init__(self, resource_group, subscription_id, credential):
        self.Client = MonitorManagementClient(
            credential, subscription_id)
        self.resource_group = resource_group
        self.subscription_id = subscription_id

    def enable(self, config_name, environment):
        current_dir = os.path.dirname(__file__)
        config_file = os.path.join(
            current_dir, "config", config_name, "app_service", "config.json")
        microservices_config_file = open(config_file)
        microservices_config = json.load(microservices_config_file)
        print(f"Loaded microservices config file {config_file}")

        for microservice in microservices_config:
            microservice_name = microservice + "-" + environment

            KeyVault.substitue_expression(microservices_config[microservice]['diagnostic-settings'])

            # Create a LogSettings object for app service console logs
            workspace_id = microservices_config[microservice]['diagnostic-settings']['workspace_id']
            log_settings = LogSettings(
                category=microservices_config[microservice]['diagnostic-settings']['category'],
                enabled=True,
                retention_policy=RetentionPolicy(
                    days=0,
                    enabled=False
                )
            )

            # Create a DiagnosticSettingsResource object
            diagnostic_setting_resource = DiagnosticSettingsResource(
                workspace_id=workspace_id,
                logs=[log_settings],
                metrics=[],
                storage_account_id=None,
                service_bus_rule_id=None
            )

            print(microservices_config[microservice]['diagnostic-settings']['name'])
            resource_uri = f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Web/sites/{microservice_name}"
            print(resource_uri)

            self.Client.diagnostic_settings.create_or_update(
                name=microservices_config[microservice]['diagnostic-settings']['name'],
                resource_uri=resource_uri,
                parameters=diagnostic_setting_resource
            )

            print("Diagnostic settings added to the app service.")