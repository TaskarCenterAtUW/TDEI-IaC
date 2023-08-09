### Referred Material

https://pypi.org/project/azure-mgmt-web/  
https://learn.microsoft.com/en-us/azure/developer/python/sdk/examples/azure-sdk-example-web-app?tabs=cmd  
https://github.com/Azure-Samples/azure-samples-python-management/tree/main/samples/appservice 

### TODO:
1. Define configurations for `Test` and `prod`
2. For now, copied "dev" config to "test" and "prod"

### Instructions
The provisioning of `app_service_plans` and `app_services` happens in the main `create-env.py` script.
`create-env.py` makes use of the `AppServicePlan` and `AppService` classes in the infra folder and the functions available inside it.  

#### Structure of AppServicePlan `config.json`
- AppServicePlans
	- Sku
	- reserved

The Sku defines the app service plan type

#### Structure of AppService `config.json`

- AppServices
    - app-service-plan
    - linux-fx-version
    - health-check-path
      - _Path_ to the health check goes here.
    - health-check-http-status
      - Expected _return http status code_ for the health check
    - application-parameters
      - All application parameters for the app services goes here
    - Diagnostic Settings
      - Log Analytics workspace id to be passed

The config.json can have multiple app services, and all the app services can be grouped under different app service plans mentioned with the app-service-plan key. 

#### How to add a app service plans
Include the app service plan name and its configurations (sku and reserved attributes) in the `app_service_plan/config.json`

#### How to add app services
Include the app services name and its configurations (app-service-plan, linux-fx-version and application-parameters) in the `app_service/config.json`


#### HOW TO RUN AFTER MAKING CHANGES
1. Set the environment.
2. From the root folder, Run `py create-env.py -e <environment> -c <ref_env> -l <location>`
3. The script "upserts" values. So, only changes are updated.
