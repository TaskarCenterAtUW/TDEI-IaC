import os
import json

class AppServicePlan:
    def __init__(self, web_client):
        self.web_client = web_client

    def provision(self, resource_group,config_name, location, environment):
        # Load configuration files
        current_dir = os.path.dirname(__file__)
        app_service_plan_config_file = os.path.join(
            current_dir, "config", config_name, "app_service_plan", "config.json")
        config_file = open(app_service_plan_config_file)
        config = json.load(config_file)
        print(f"Loaded app service plan config file {app_service_plan_config_file}")
        print("Creating app service plans..")
        for app_service_plan in config:
            app_service_plan_name = app_service_plan['plan-name'] + "-" + environment  
            plan_result = self.web_client.app_service_plans.begin_create_or_update(
                resource_group,
                app_service_plan_name,
                {
                    "location": location,
                    "reserved" : app_service_plan['reserved'],
                    "sku" : app_service_plan['sku']
                }
            ).result()
            print(f"Service plan {app_service_plan_name} create with plan id: {plan_result.id}")
