### Referred Material
https://pypi.org/project/azure-mgmt-servicebus/  
https://learn.microsoft.com/en-us/samples/azure-samples/azure-samples-python-management/servicebus/  
https://github.com/azure-samples/azure-samples-python-management/tree/main/samples/servicebus 

### TODO:
1. Define configurations for `Test` and `prod`
2. For now, copied "dev" config to "test" and "prod"

### Instructions
The provisioning of `service bus` happens in the main `create-env.py` script.  
`create-env.py` makes use of the `ServiceBus` class in this folder and the functions available inside it.

#### Structure of `config.json`
- Service bus
  - Queues
  - Topics
    - Subscriptions

Within a Service bus, there can be multiple queues and multiple topics.  
Each topic can have zero or more subscriptions. 

#### How to add a new topic
Include the topic name and its configuration in place

#### How to modify the configuration of a new topic
Make the changes to the `config.json` and save

#### HOW TO RUN AFTER MAKING CHANGES
1. Set the environment.
2. From the root folder, Run `py create-env.py -e <environment> -c <ref_env> -l <location>`
3. The script "upserts" values. So, only changes are updated.