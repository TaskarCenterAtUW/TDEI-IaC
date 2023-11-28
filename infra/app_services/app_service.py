import json
import os
import subprocess
from infra.keyvault.keyvault import KeyVault

class AppService:
    def __init__(self, web_client, resource_group, subscription_id):
        self.web_client = web_client
        self.resource_group = resource_group
        self.subscription_id = subscription_id

    def __execute_command(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        response = process.communicate()
        json_message = response[0].decode()
        return (process.returncode, '' if json_message == '' else json.loads(json_message))

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

            # Assigning the subnet equivalent of App service plan. Can include this in the config
            if microservices_config[microservice]['vnet-enabled'] is False:
                subnet = None
            else:
                vnet = f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Network/virtualNetworks/TDEI-" + environment + "-VNET/subnets/"
                subnet = vnet + microservices_config[microservice]['app-service-plan'] + "-subnet"

            if microservices_config[microservice]['publicNetworkAccess'] is None:
                public_access = None
            else:
                public_access = microservices_config[microservice]['publicNetworkAccess']

            print(f"Provisioning App Service: {microservice_name}")
            web_app_result = self.web_client.web_apps.begin_create_or_update(
                self.resource_group,
                microservice_name,
                {
                    "location": location,
                    "server_farm_id": app_service_plan.id,
                    "vnetRouteAllEnabled": microservices_config[microservice]['vnet-enabled'],
                    "virtualNetworkSubnetId": subnet,
                    "publicNetworkAccess": public_access,
                    "site_config": {
                        "linux_fx_version": microservices_config[microservice]['linux-fx-version'],
                        "always_on": microservices_config[microservice]['always-on']
                    },
                }
            ).result()
            print(f"Completed - {web_app_result.default_host_name}. Configuring Health Check for it")
            print(f"Completed -Id is  {web_app_result.id}.")
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

            # Cors Settings. If cors needs an array, loop through the array
            if "cors-settings" in microservices_config[microservice]:
                command = 'az webapp cors add --resource-group ' + self.resource_group + ' --name ' + microservice_name + ' --allowed-origins ' + microservices_config[microservice]['cors-settings']['allowed-origins']
                return_code, result = self.__execute_command(command)
                if return_code == 0:
                    print(result)
                else:
                    print('Failed to create CORS')

            if microservices_config[microservice]['vnet-enabled'] is True:
                # Provisioning Private Endpoint Connection
                pe_command = 'az network private-endpoint create --resource-group ' + self.resource_group + ' --name ' + microservice_name + '-pe --vnet-name ' + 'TDEI-' + environment + '-VNET --subnet TDEI-pe-subnet --private-connection-resource-id ' + web_app_result.id + ' --connection-name ' + microservice_name + 'plsc --group-id sites'
                print(pe_command)
                return_code, result = self.__execute_command(pe_command)
                if return_code == 0:
                    print(result)
                else:
                    print('Failed to create private endpoint')


