import getopt
import sys
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.identity import DefaultAzureCredential
from infra import KeyVault, VirtualNetworks, ServiceBus, StorageAccount, PostgreSQLService, AppServicePlan, LogAnalytics
from infra import AppService, AppServiceParameters, DiagnosticSettings
from infra import ContainerInstaces
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.rdbms.postgresql_flexibleservers import PostgreSQLManagementClient


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
        container_client = ContainerInstanceManagementClient(credential=DefaultAzureCredential(),
            subscription_id=subscription_id)
        postgres_client = PostgreSQLManagementClient(credential=DefaultAzureCredential(),
            subscription_id=subscription_id)

        RESOURCE_GROUP_NAME = "GaussianRG-" + environment

        app_services = web_client.web_apps.list_by_resource_group(RESOURCE_GROUP_NAME)

        print(f"App Services in Resource Group: {RESOURCE_GROUP_NAME}")

        for app_service in app_services:
            app_status = web_client.web_apps.get(RESOURCE_GROUP_NAME, app_service.name)
            print(f" App Service: {app_service.name} - Status: {app_status.state}")

        print(f"Function apps in Resource Group: {RESOURCE_GROUP_NAME}")

        function_apps = web_client.web_apps.list_by_resource_group(RESOURCE_GROUP_NAME)
        for function_app in function_apps:
            if 'functionapp' in function_app.kind:
                function_status = web_client.web_apps.get(RESOURCE_GROUP_NAME, function_app.name)
                print(f"  Azure Function: {function_app.name} - Status: {function_status.state}")

        print(f"Postgres servers in Resource Group: {RESOURCE_GROUP_NAME}")

        postgres_servers = postgres_client.servers.list_by_resource_group(RESOURCE_GROUP_NAME)

        for server in postgres_servers:
            print(f"  PostgreSQL Server: {server.name} - Status: {server.state}")


        print(f"Container instances in Resource Group: {RESOURCE_GROUP_NAME}")

        container_groups = container_client.container_groups.list_by_resource_group(RESOURCE_GROUP_NAME)
        for container in container_groups:
            container_view = container_client.container_groups.get(RESOURCE_GROUP_NAME, container.name).instance_view
            if container_view is not None and container_view.state is not None:
                print(f"  Container Instance: {container.name} - Status: {container_view.state}")
            else:
                print(f"  Container Instance: {container.name} - Status: Unknown (No instance view available)")
    
        
    else:
        show_help() 
