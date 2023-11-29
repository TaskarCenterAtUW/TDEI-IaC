### Referred Material
https://pypi.org/project/azure-mgmt-network/  
https://learn.microsoft.com/en-us/samples/azure-samples/azure-samples-python-management/network/    
https://github.com/Azure-Samples/azure-samples-python-management/tree/main/samples/network/  
https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/network/azure-mgmt-network/generated_samples/

### TODO:
1. Define configurations for `Test` and `prod`
2. For now, copied "dev" config to "test" and "prod"

### Instructions
The provisioning of `Virtual Network` happens in the main `create-env.py` script.  
`create-env.py` makes use of the `VirtualNet` class in this folder and the functions available inside it.

#### Information on Vnet
Within a Virtual Network, there are "address spaces", which are further divided into different "subnets".  
So, we create one VNet for each environment. 

**Address Space:**

The address space in Azure VNet refers to the range of IP addresses that are available for allocation to resources within the virtual network.  
It's defined as a CIDR block (Classless Inter-Domain Routing) and represents the entire pool of IP addresses available within the VNet.

This address space defines the overall range of IP addresses that the VNet can use.  
For example, an address space of 10.0.0.0/16 allows for the allocation of IP addresses ranging from 10.0.0.0 to 10.0.255.255.

**Subnets:**

Subnets are subdivisions of the address space defined within the VNet.  
They allow to segment the VNet's address space into smaller, more manageable chunks.

Each subnet within a VNet is a contiguous range of IP addresses allocated from the VNet's address space.  
These subnets are used to organize resources and apply network security and access controls.

**Relationship:**
The address space defines the total range of IP addresses available within the VNet.
Subnets are carved out of the defined address space and are used to logically partition and organize resources within the VNet.
Each subnet gets a range of IP addresses that fall within the overall address space of the VNet.
Resources deployed within a specific subnet can communicate with each other directly, and you can apply network security rules, route tables, etc., at the subnet level.
For example, if you have an address space of 10.0.0.0/16, you could create subnets like 10.0.1.0/24 and 10.0.2.0/24, which are both within the 10.0.0.0/16 range but are distinct subranges within that space. Resources in the 10.0.1.0/24 subnet can communicate with each other directly but might be segregated from resources in the 10.0.2.0/24 subnet based on network security rules.

#### Structure of `config.json`
- Virtual Network
    - Address Space
    - Subnets

#### HOW TO RUN AFTER MAKING CHANGES
1. Set the environment.
2. From the root folder, Run `py create-env.py -e <environment> -c <ref_env> -l <location>`
3. The script "upserts" values. So, only changes are updated.

**NOTE**: Please ensure the availability of address space between various VNets in the subscription group