### Referred Material
https://pypi.org/project/azure-mgmt-storage/
https://learn.microsoft.com/en-us/azure/developer/python/sdk/examples/azure-sdk-example-storage?tabs=cmd
https://github.com/Azure-Samples/azure-samples-python-management/blob/main/samples/storage/

### TODO:
1. Define configurations for `Test` and `prod`
2. For now, copied "dev" config to "test" and "prod"

### Instructions
The provisioning of `storage account` and `storage containers` happens in the main `create-env.py` script.  
`create-env.py` makes use of the `StorageAccountService` class in this folder and the functions available inside it.

#### Structure of `config.json`
- Storage account
  - Sku
  - Containers

The Sku defines the storage account type (https://learn.microsoft.com/en-us/rest/api/storagerp/srp_sku_types).
Within a Storage account, there can be multiple containers to store the blob objects.  


#### How to add a storage account
Include the storage account name and its configurations (sku and containers) in the storage_account.config.json

#### How to modify the configuration of a new topic
Make the changes to the `storage_account.config.json` and save

#### HOW TO RUN AFTER MAKING CHANGES
1. Set the environment.
2. From the root folder, Run `py create-env.py -e <environment> -c <ref_env> -l <location>`
3. The script "upserts" values. So, only changes are updated.

#### Storage connection string   
After provisioning the storage account the connection string is stored in keyvault with the key name `storage-connection-string`. It can be access in app_services config.json with the expression `{storage-connection-string}`