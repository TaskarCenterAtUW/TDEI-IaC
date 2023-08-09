# Approach
Inside the `.github/workflows` folder, there will be 3 workflows:
1. provision-infrastructure
2. delete-infrastructure
3. clone-infrastructure (this will be part of V3)

Each of these do what their name suggests.

### Workflow
- Each component of the infrastructure will have its own folder.
    - Within each component, configuration for each of the `dev`, `test`, `stage` and `prod` environment are stored, in their respective folder.
    - The secrets for each of these are also stored in encrypted format using `ansible vault`
- From the main script, calls to the individual components shall be made and the components provisioned.
- All the endpoints, connection strings, component names etc, that are created/provisioned are captured in variables and these variables are used wherever required

### PS:
We clearly differentiate the role of InfraAdmin and a Developer in our approach.  
InfraAdmin provides the necessary infrastructure for developers to run their stuff.  
It is the responsibility of the developers to deploy and maintain their services.

Instructions on how to add / modify a component of infrastructure shall be provided.

### Why AZ CLI And not Terraform
1. TDEI system does not have complex infrastructure needs where the state of the system needs to be maintained.
2. Easier and faster to develop with AZ CLI over Python
3. Ultimately the System will be maintained by UW team. They would need a resource with knowledge on Terraform. By just using AZ CLI SDK with Python, this can be eliminated
