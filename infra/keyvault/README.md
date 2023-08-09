### Referred Material
https://pypi.org/project/azure-keyvault-secrets/  
https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python?tabs=azure-cli  
https://github.com/Azure-Samples/azure-samples-python-management/tree/main/samples/keyvault  
https://learn.microsoft.com/en-us/cli/azure/keyvault/secret?view=azure-cli-latest#az-keyvault-secret-list  


### Instructions
The provisioning of `key_vault` happens in the main `create-env.py` script.  
`create-env.py` makes use of the `KeyVault` class in this infra/keyvault folder and the functions available inside it.

#### How to create and retrive secrets in KeyVault

- Import the KeyVault Service  

`from infra.keyvault.keyvault import KeyVault`

- To create a secret value in the KeyVault

`KeyVault.setSecret('key_name', 'value_name')`

- To retrieve a secret value from KeyVault

`KeyVault.getSecret('key_name').value`

- To replace a tokens in config with KeyVault secret
`KeyVault.substitue_expression(json)`
The json object has to be in dictionary format with the tokens to be replaced in between `{}`


#### HOW TO RUN AFTER MAKING CHANGES
1. Set the environment.
2. From the root folder, Run `py create-env.py -e <environment> -c <ref_env> -l <location>`
3. The script "upserts" values. So, only changes are updated.


#### List of Keys and the location where they are used
| Key | Set In | Used in |
| ------ | ------ |-------|
| _tdei-loganalytics-workspace-id_ | `loganalytics.py` |appservices config for enabling diagnostic settings|
| _loggerdb-connection-string_ | `loggerdb.py` |appservices config for connecting to logger db|
| _service-bus-connection-string_ | `service_bus.py` |appservices config for connecting to service bus|
| _storage-connection-string_ | `storage_services.py` |appservices config for connecting to storage|


### Encoding / Decoding secrets file
The repository has only the encoded secrets file. To view the secrets, one should decode it.  
Command to decode :  
`ansible-vault decrypt secrets.json.enc --output secrets.json`  
This will prompt for a password. Right now, all the secrets are encoded with a single key.  
This key is present in the Git Repo secret as `ANSIVAULT-KEY`  

If any change is to be made to the secrets value, decode the file, make the change in the decoded file, then encrypt again with the key.  
`ansible-vault encrypt secrets.json --output secrets.json.enc`  
This will prompt for a password. This is the ANSIVAULT_KEY.  
You could provide a new password. But **remember** to edit the ANSIVAULT_KEY git repo secret to reflect this new value. 