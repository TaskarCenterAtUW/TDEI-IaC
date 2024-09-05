# TDEI-IaC
Maintaining Infrastructure as Code

### Setup Python environment
`py -3 -m venv .venv`  
`.venv\Scripts\activate`  
`.\.venv\Scripts\python.exe -m pip install --upgrade pip`  
`pip install -r requirements.txt`

### How to run the code locally
Instructions are provided in the [Documentaion](Documentation/Instructions.md) in the section _to provision PROD environment_

### Directory structure
1. Each azure cloud component has its own folder under `infra`
2. Each component has `dev`, `test`, `stage` and `prod` configurations available
3. Instructions on how to add a new component / change an existing configuration are provided in the individual folders

### Manual steps involved post prod deployment

1. Reset TDEI admin user password on key cloak dashboard
2. Regenerate keycloak client secret for tdei-gateway client and update the Auth-n-z service configuration

### STATUS
The following services are provisioned at present from the github workflow:

- [x] Resource Group
    - [x] Keyvault to store DB credentials etc.
        - [x] Keyvault to set secrets and endpoints and use them in application parameters
    - [x] PostgreSQL Flexible Instance
        - [x] Create databases from config
    - [x] Application Insights
        - [x] Log Analytics workspace
        - [x] Diagnostic Settings enabled for App Services
    - [x] Storage Account
        - [x] Storage containers
    - [x] Service Bus
        - [x] Queue
        - [x] Topics
        - [x] Subscriptions
    - [x] cosmosDB
    - [x] App Service Plan
    - [x] App Services
        - [x] Application Parameters
        - [x] Health Checks
        - [x] Diagnostic settings
