import getopt
import sys
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.identity import DefaultAzureCredential

def show_help():
    print("Displaying Help")
    exit()

if __name__ == "__main__":
    argumentList = sys.argv[1:]
    options = "h:e:s:"
    long_options = ["Help", "environment=", "subscription="]

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        # checking each argument
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-h", "--Help"):
                show_help()
            elif currentArgument in ("-e", "--environment"):
                environment = currentValue
            elif currentArgument in ("-s", "--subscription"):
                subscription_id = currentValue
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
        exit(1)

    if (environment):
        print("Acquiring azure credential object..")
        # Acquire a credential object using CLI-based authentication.
        credential = AzureCliCredential()

        resource_client = ResourceManagementClient(credential, subscription_id)
        web_client = WebSiteManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=subscription_id
        )

        print("Checking if Resource Group Environment Exists..")
        resource_group_exists = resource_client.resource_groups.check_existence(
            resource_group_name=environment
        )
        if resource_group_exists:
            print(f"Resource group '{environment}' exists. Deleting it now")
            delete_poller = resource_client.resource_groups.begin_delete(
                resource_group_name=environment,
                polling=True,
                polling_interval=5
            )
            delete_poller.wait()

            print(f"Deleted resource group: {environment}")

        else:
            print(f"Resource group '{environment}' does not exist. Please Enter a valid name")

    else:
        show_help()