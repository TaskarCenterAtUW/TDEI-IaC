### Guidelines

1. Within Azure, GS would Create one resource group per environment that needs to be provisioned.
    1. Example: RG-Dev for Dev environment, RG-Test for Test environment and so on.
2. This is needed so that only a minimal change to be done in the code/configuration files in order to provision a new environment.
    1. This also helps us to reuse the same variables across environments.
    2. All one would need to do is to set the right environment -> this is also useful in CI/CD and Devops pipelines to deploy code to different environments.

