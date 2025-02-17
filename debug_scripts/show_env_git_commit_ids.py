# Pre-requisites: Install Azure SDK for Python
# brew update && brew install azure-cli
# az login
# az account set --subscription "YOUR_SUBSCRIPTION_ID"
# az account list --output table
# ###
import csv
import re
from azure.identity import DefaultAzureCredential
from azure.mgmt.web import WebSiteManagementClient
import os
from dotenv import load_dotenv
# from tqdm import tqdm


# Load environment variables from a .env file
load_dotenv()

print("Collecting App Services and their Docker images...")

# Get the subscription ID from the environment variables
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")

if not subscription_id:
    raise ValueError("AZURE_SUBSCRIPTION_ID environment variable is not set")
else:
    print(f"Proceeding with the Subscription ID: {subscription_id}")

# Initialize Azure authentication
credential = DefaultAzureCredential()
    # exit(1)
# Initialize the WebSiteManagementClient
web_client = WebSiteManagementClient(credential, subscription_id)

# Define resource groups to check
environment_resource_groups = [
    "GaussianRG",
    "GaussianRG-prod",
    "GaussianRG-stage"
]

# Prepare the CSV file
csv_file = "app_services_docker_images.csv"
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(["App Service Name", "Resource Group", "Docker Image", "Commit ID"])

    # Collect data and write to CSV
    for resource_group in environment_resource_groups:
        app_services = web_client.web_apps.list_by_resource_group(resource_group)
        
        total_app_services = len(list(app_services))
        print(f"Getting commit IDs for the {total_app_services} App Services in the {resource_group} resource group")
        for app_service in app_services:
            app_service_name = app_service.name
            docker_image = "No Docker image deployed."
            commit_id = "N/A"
            
            # Get configuration details of the App Service
            config = web_client.web_apps.get_configuration(resource_group, app_service_name)
            
            if config.linux_fx_version and "DOCKER" in config.linux_fx_version.upper():
                docker_image = config.linux_fx_version.replace("DOCKER|", "")
                # Extract commit ID if available
                match = re.search(r":(.+)$", docker_image)
                # print(app_service_name, match)
                if match:
                    commit_id = match.group(1)
                    if commit_id.endswith('.'):
                        commit_id = commit_id[:-1]            
            # Write the row to the CSV file
            writer.writerow([app_service_name, resource_group, docker_image, commit_id])

print(f"App Services and their Docker images have been written to {csv_file}")
# Read the CSV file and create separate CSVs for each resource group
with open(csv_file, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    dev_rows = []
    prod_rows = []
    stage_rows = []

    for row in reader:
        if row["Commit ID"] and not row["Commit ID"].endswith("latest"):
            if row["Resource Group"] == "GaussianRG":
                dev_rows.append(row)
            elif row["Resource Group"] == "GaussianRG-prod":
                prod_rows.append(row)
            elif row["Resource Group"] == "GaussianRG-stage":
                stage_rows.append(row)

    # Write to dev_env.csv
    with open("dev_env.csv", mode='w', newline='') as dev_file:
        writer = csv.DictWriter(dev_file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(dev_rows)
        print("Done writing Dev environment AppServices and their Docker images to dev_env.csv")

    # Write to prod_env.csv
    with open("prod_env.csv", mode='w', newline='') as prod_file:
        writer = csv.DictWriter(prod_file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(prod_rows)
        print("Done writing Production environment AppServices and their Docker images to prod_env.csv")

    # Write to stage_env.csv
    with open("stage_env.csv", mode='w', newline='') as stage_file:
        writer = csv.DictWriter(stage_file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(stage_rows)
        print("Done writing Stage environment AppServices and their Docker images to stage_env.csv")


