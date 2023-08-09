import json
import os
from azure.mgmt.web.models import NameValuePair
from infra.keyvault.keyvault import KeyVault


class AppServiceParameters:
    def __init__(self, web_client, resource_group):
        self.web_client = web_client
        self.resource_group = resource_group

    def update_configuration(self, config_name, environment):
        # Load microservices config.json
        current_dir = os.path.dirname(__file__)
        config_file = os.path.join(
            current_dir, "config", config_name, "app_service", "config.json")
        microservices_config_file = open(config_file)
        microservices_config = json.load(microservices_config_file)
        print(f"Loaded microservices config file {config_file}")

        # Replace variables with KeyVault values
        for microservice in microservices_config:
            KeyVault.substitue_expression(microservices_config[microservice]['application-parameters'])
            # Extract log analytics workspace name
            log_analytics_workspace_variable = microservices_config[microservice]['diagnostic-settings']['workspace_id']
            key_vault_key = log_analytics_workspace_variable[1:-1].strip()
            try:
                key_vault_value = microservices_config[microservice]['diagnostic-settings']['workspace_id']
                microservices_config[microservice]['diagnostic-settings']['workspace_id'] = key_vault_value.replace("{"+key_vault_key+"}", KeyVault.getSecret(key_vault_key).value)
            except Exception as e:
                print (f"Failed to fetch keyvault key {key_vault_key}")
                print (e)
                return(1)
            # Build application parameters for the AppService
            microservice_name = microservice + "-" + environment
            application_parameters = []
            for application_parameter in microservices_config[microservice]["application-parameters"]:
                application_parameters.append(NameValuePair(
                    name=application_parameter, value=microservices_config[microservice]["application-parameters"][application_parameter]))
            print(
                f"Update App Service application parameters: {microservice_name}")
            self.web_client.web_apps.update_configuration(self.resource_group, microservice_name, {
                "app_settings": application_parameters
            })
        
        
