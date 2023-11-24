import json
import os
from infra.keyvault.keyvault import KeyVault

class AppService:
    def __init__(self, web_client, resource_group):
        self.web_client = web_client
        self.resource_group = resource_group

    def provision(self, config_name, location, environment):
        # Load microservices config.json
        current_dir = os.path.dirname(__file__)
        config_file = os.path.join(
            current_dir, "config", config_name, "app_service", "config.json")
        microservices_config_file = open(config_file)
        microservices_config = json.load(microservices_config_file)
        print(f"Loaded microservices config file {config_file}")

        for microservice in microservices_config:
            microservice_name = microservice + "-" + environment

            # Fetch the AppServicePlan Id
            app_service_plan = self.web_client.app_service_plans.get(
                self.resource_group,
                microservices_config[microservice]['app-service-plan'] + "-" + environment 
            )

            print(f"Provisioning App Service: {microservice_name}")
            web_app_result = self.web_client.web_apps.begin_create_or_update(
                self.resource_group,
                microservice_name,
                {
                    "location": location,
                    "server_farm_id": app_service_plan.id,
                    "vnetRouteAllEnabled": microservices_config[microservice]['vnet-enabled'],
                    "site_config": {
                        "linux_fx_version": microservices_config[microservice]['linux-fx-version'],
                        "always_on": microservices_config[microservice]['always-on']
                    },
                }
            ).result()
            print(
                f"Completed - {web_app_result.default_host_name}. Configuring Health Check for it")
            KeyVault.setSecret(microservice + '-hostname', web_app_result.default_host_name)
            site_config = self.web_client.web_apps.get_configuration(self.resource_group, microservice_name)

            # Not all app services have health check. Example: API-gateway-spec
            if "health-check-path" in microservices_config[microservice]:
                site_config.health_check_path = microservices_config[microservice]['health-check-path']
                site_config.health_check_http_status = microservices_config[microservice]['health-check-http-status']

            # Keycloak service requires a startup command line
            if "appCommandLine" in microservices_config[microservice]:
                site_config.appCommandLine = microservices_config[microservice]['appCommandLine']

            self.web_client.web_apps.update_configuration(self.resource_group, microservice_name, site_config)
            print("Completed Configuring Health Check")

