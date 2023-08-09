### Referred Material
For Log Analytics - https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/loganalytics/azure-mgmt-loganalytics/generated_samples
### TODO:
1. Define configurations for `Test` and `prod`
2. For now, copied "dev" config to "test" and "prod"
3. Change the config file to a JSON array if more than one Analytics space to be provisione

### Instructions
The provisioning of `LogAnalyticsWorkspace` happens in the main `create-env.py` script.

#### Structure of `config.json`
Self Explanatory

#### How to add a new space
Change the existing config to use a Json array instead of object

#### How to modify the configuration of an existing database or collection
Make the changes to the `config.json` and save

#### HOW TO RUN AFTER MAKING CHANGES
1. Set the environment.
2. From the root folder, Run `py create-env.py -e <environment> -c <ref_env> -l <location>`
3. The script "upserts" values. So, only changes are updated.