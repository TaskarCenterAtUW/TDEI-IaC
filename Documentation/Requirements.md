## Requirements
1. All infrastructure must be provisioned using scripts and must be automated.
2. No manual steps needed, except for “confirming” the action (create / destroy / replace)
3. The code must be easy to understand and easy to maintain
4. No hard coding of literals / connection strings / passwords should be present
5. Secrets that are used within the services must also be loaded via IaC.
6. The code must also be extensible in the way that - if the cloud provider is changed in the future, adjusting the code to use the new cloud provider’s components must be easy.
7. In this case, minimal changes to be made in a certain configuration file that represent the “type of component” needed (AWS - EC2, S3 as compared to Azure - APP Service Plan, Storage container).
8. And necessary permission settings to be made
9. All steps on how to create / destroy an environment must be well documented.
10. Steps must also be documented on how to add and integrate a new component into an existing environment.


To be able to achieve this, there are certain [guidelines](Guidelines.md)

### Scope of V2
This section lists the tasks that are under the scope of "Infrastructure as Code - V2":
1. Provision infrastructure for an environment using scripts:
    1. Environments supported: DEV, TEST / STAGE and PROD
    2. By provisioning the infrastructure, we mean provisioning the
        1. Resource Group
        2. Blob Storage and containers
        3. PostgreSql database
        4. Event bus / Message bus and topics
        5. Logger database
        6. App Service Plans and App services
        7. Secrets Handling
2. Delete an environment using scripts
3. Provision another environment with same infra config as one of the DEV, TEST or PROD environments

### Scope of V3
1. Provision  virtualNet, Address space, Subnets using IaC  
2. Adjust code to put app services inside the Virtual Network  
   -  Test every github repo workflow if they work well with this change

### Out of Scope for V3 - In Scope for V4
This section lists the tasks that are **out of scope** for "Infrastructure as Code - V2":

1. Cloning an environment to "replicate" a bug in that environment.
2. CI/CD for app services. How do the git workflows in each repo change?
