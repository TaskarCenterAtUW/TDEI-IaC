import getopt
import sys
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.identity import DefaultAzureCredential
from infra import StorageAccount, AppService, AppServiceParameters, AppServicePlan, PostgreSQLService, KeyVault
from infra import ServiceBus, LogAnalytics, DiagnosticSettings, VirtualNetworks


def show_help():
    print("Displaying Help")
    exit()


if __name__ == "__main__":
    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]

    # Options
    options = "h:e:c:l:s:"
    # Long options
    long_options = ["Help", "environment=", "config_name=", "location=", "subscription="]

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        # checking each argument
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-h", "--Help"):
                show_help()
            elif currentArgument in ("-e", "--environment"):
                environment = currentValue
            elif currentArgument in ("-c", "--config"):
                config = currentValue
            elif currentArgument in ("-l", "--location"):
                location = currentValue
            elif currentArgument in ("-s", "--subscription"):
                subscription_id = currentValue
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
        exit(1)

    if environment.islower() is False:
        print("Please enter the environment name in lower case letters")
        # This env is used for provisioning postgres instance, that cannot take Upper letters
        quit()

    if (environment and config and location):
        print("Acquiring azure credential object..")
        # Acquire a credential object using CLI-based authentication.
        credential = AzureCliCredential()
        resource_client = ResourceManagementClient(credential, subscription_id)
        web_client = WebSiteManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=subscription_id
        )

        RESOURCE_GROUP_NAME = "GaussianRG-" + environment

        # Provision the resource group.
        print("Provisioning Resource Group..")
        rg_result = resource_client.resource_groups.create_or_update(
            RESOURCE_GROUP_NAME, {"location": location}
        )

        print(
            f"Provisioned resource group {rg_result.name} in the \
        {rg_result.location} region"
        )

        # Create Keyvault to store credentials and application parameters needed by AppServices
        KeyVault.initialize(credential, RESOURCE_GROUP_NAME, environment)

        # Set secrets in KeyVault
        KeyVault.store_secrets(config_name=config)

        # Provision Virtual Network
        virtual_network = VirtualNetworks(
            subscription_id=subscription_id, resource_group=RESOURCE_GROUP_NAME, credential=credential)
        virtual_network.provision(
            config_name=config,
            location=location,
            environment=environment
        )

        #Provision PostgreSQL Flexible Server
        postgresql_service = PostgreSQLService(
            credential=credential, subscription_id=subscription_id, resource_group=RESOURCE_GROUP_NAME)
        postgresql_service.provision(
            environment=environment,
            config_name=config,
            location=location
        )

        # Provision Storage Account
        storage_account = StorageAccount(
            subscription_id=subscription_id, resource_group=RESOURCE_GROUP_NAME, credential=credential)
        storage_account.provision(
            config_name=config,
            environment=environment,
            location=location
        )

        # Provision Service Bus and Queues
        service_bus = ServiceBus(
            credential=credential, subscription_id=subscription_id, resource_group=RESOURCE_GROUP_NAME)
        service_bus.provision(
            config_name=config,
            environment=environment,
            location=location
        )
        print("service bus: provisioned")

        # Provision Log Analytics workspace and Application Insights
        logAnalytics = LogAnalytics(credential=credential, subscription_id=subscription_id, resource_group=RESOURCE_GROUP_NAME)
        logAnalytics.provision(
            config_name=config,
            location=location
        )
        print("Log analytics Workspace: provisioned")

        # Provision AppServicePlan
        app_service_plan = AppServicePlan(web_client)
        print("Provisioning AppService Plan..")
        app_service_plan.provision(
            resource_group=RESOURCE_GROUP_NAME,
            config_name=config,
            environment=environment,
            location=location
        )

        # Provision AppServices
        app_service = AppService(web_client, RESOURCE_GROUP_NAME, subscription_id)
        app_service.provision(
            config_name=config,
            environment=environment,
            location=location
        )

        # Set AppServices Application Parameters
        app_service_params = AppServiceParameters(web_client, RESOURCE_GROUP_NAME)
        app_service_params.update_configuration(
            config_name=config,
            environment=environment
        )

        #Enable Diagnostic settings for App Services
        print("Enabling Diagnostic Settings for App Services ")
        diagSettings = DiagnosticSettings(credential=credential, subscription_id=subscription_id, resource_group=RESOURCE_GROUP_NAME)
        diagSettings.enable(config_name=config, environment=environment)

    else:
        show_help()
