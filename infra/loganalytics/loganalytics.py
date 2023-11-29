import json
import os
from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
from azure.mgmt.applicationinsights.models import ApplicationInsightsComponent, ApplicationType
from infra.keyvault.keyvault import KeyVault

class LogAnalytics:
    def __init__(self, credential, subscription_id, resource_group):
        self.logAnalyticsClient = LogAnalyticsManagementClient(
            credential=credential,
            subscription_id=subscription_id)

        self.appInsightsClient = ApplicationInsightsManagementClient(
            credential=credential,
            subscription_id=subscription_id)

        self.resource_group = resource_group


    def provision(self, config_name, location):
        # Load configuration files
        current_dir = os.path.dirname(__file__)
        config_file = os.path.join(current_dir, "config", config_name, "config.json")
        config_file = open(config_file)
        config = json.load(config_file)

        # Provision Account first
        response = self.logAnalyticsClient.workspaces.begin_create_or_update(
            resource_group_name=self.resource_group,
            workspace_name=config['logAnalytics']['workSpaceName'],
            parameters={
                "location": location,
                "properties": config['logAnalytics']['properties'],
                "tags": config['logAnalytics']['tags']
            }
        ).result()

        KeyVault.setSecret('tdei-loganalytics-workspace-id', response.id)

        # Provision Application Insights Next
        # Define the properties of the Application Insights component
        app_insights_component = ApplicationInsightsComponent(
            location=location,
            application_type=ApplicationType.web,
            workspace_resource_id=response.id, # https://github.com/Azure/azure-cli/issues/6949
            # Resource id is a mandatory field, and the whole id should be passed, not just the name
            kind=ApplicationType.web
        )

        # Create the Application Insights component
        self.appInsightsClient.components.create_or_update(self.resource_group, config['appInsights']['name'], app_insights_component)

        print("Application Insights component created successfully.")
