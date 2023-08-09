# Things to note
 - This git repo contains the code to provision infrastructure for an environment.  
 - Only two people can run the workflows at the moment `rdevalap` and `uwtcat`
 - If any other person initiates the `github action` to provision or destroy infrastructure, the workflow is triggered but the jobs are skipped. No log can be viewed
 - The _secrets_ such as `postgres database password` and etc are stored in an encrypted format in the repository
   - These can be decrypted using the encryption key stored in the git repo secrets: `ANSIVAULT_KEY`
   - In case a secret needs to be changed, decrypt the files, change the secret value, encrypt the file and rerun the workflow / github action

## How to provision infrastructure
 - Ensure the right configurations are set for each components under _infra_ folder
 - Run the github action `provision infrastructure`
 - Make sure to provide the right `environment` name and the `configuration` it should pick

## How to make changes to configurations
 - Developers make the necessary changes to the configurations
 - Developers raise a PR to the `administrator` of this repository
 - At the moment, `rdevalap` and `uwtcat` are the administrators. 
 - Administrators review the PR, and if everything looks good, approve the PR and apply the changed configurations

## How to add the infrastructure required for a new microservice
- On DEV System / environment
  - Developers create the new microservice
  - Developers provision the infrastructure required from within the Azure portal UI
  - After successful implementation and testing (unit and integration) of the microservice in DEV environment
    - developers should add the respective new components in the right place. Eg:
      - A new topic created for the microservice -> `infra/service_bus`
      - A new database created for the microservice -> `infra/rdbms`
    - All the required _app service parameters_ and _diagnostic settings_ to be added in the _app service_ configuration
    - Changes to be added to all the four configurations: `dev`, `test`, `stage` and `prod`
      - Alternatively, changes made to the `dev` configuration can be copied to others.
    - After finishing all the changes, raise a PR and submit to the `administrators` of the repo for review
  - Administrators review the PR, and if everything looks good, approve the PR and apply the changed configurations
