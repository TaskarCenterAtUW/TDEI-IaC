### Referred Material
https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cosmos/azure-cosmos/azure  
https://learn.microsoft.com/en-us/python/api/overview/azure/cosmos-db?view=azure-python  
https://pypi.org/project/azure-cosmos/  
https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-mgmt-cosmosdb/generated_samples/cosmos_db_mongo_db_collection_create_update.py  
https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-mgmt-cosmosdb/azure/mgmt/cosmosdb/models/_cosmos_db_management_client_enums.py
### TODO:
1. Define configurations for `Test` and `prod`
2. For now, copied "dev" config to "test" and "prod"
3. Change the config file to a JSON array if more than one DB to be provisioned. And loop through the array

### Instructions
The provisioning of `cosmosdb` happens in the main `create-env.py` script.  
`create-env.py` makes use of the `CosmosDB` class in this folder and the functions available inside it.

#### Structure of `config.json`
- Database Account
  - Database - Kind = MongoDB
  - Collection

#### How to add a new collection
Change the existing config to use a Json array at _collectionNames_ and loop through the array to provision

#### How to modify the configuration of an existing database or collection
Make the changes to the _createUpdateParameters_ in the `config.json` and save

#### HOW TO RUN AFTER MAKING CHANGES
1. Set the environment.
2. From the root folder, Run `py create-env.py -e <environment> -c <ref_env> -l <location>`
3. The script "upserts" values. So, only changes are updated.

### **NOTE**
The _mongodb_ and _collection_ name given here in the config should match the names in the app service config