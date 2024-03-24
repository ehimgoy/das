import json
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

def get_azure_instance_metadata():
    credential = DefaultAzureCredential()
    subscription_id = "a3f68f16*******************" #Enter your subscription id
    vm_name = "swazhg01" # Enter your vm name
    
    compute_client = ComputeManagementClient(credential, subscription_id)
    try:
        # List all virtual machines
        vms = compute_client.virtual_machines.list_all()
        # Filter out the desired virtual machine based on its name
        for vm in vms:
            if vm.name == vm_name:
                # Extract relevant metadata
                metadata = {
                    "name": vm.name,
                    "location": vm.location,
                    "resource_group": vm.id.split("/")[4],
                    "tags": vm.tags
                }
                return metadata
        print(f"Virtual machine '{vm_name}' not found.")
        return None
    except HttpResponseError as e:
        print(f"Failed to retrieve metadata: {str(e)}")
        return None

def get_azure_instance_metadata_key(key):
    metadata = get_azure_instance_metadata()
    if metadata:
        if key in metadata:
            return {key: metadata[key]}
        else:
            print(f"Key '{key}' not found in metadata.")
    return None

# Example usage
if __name__ == "__main__":
    # Retrieve all metadata
    azure_metadata = get_azure_instance_metadata()
    if azure_metadata:
        print("All metadata:")
        print(json.dumps(azure_metadata, indent=4))

        # Retrieve specific metadata key
        key_to_retrieve = "location"
        specific_metadata = get_azure_instance_metadata_key(key_to_retrieve)
        if specific_metadata:
            print(f"\nMetadata for key '{key_to_retrieve}':")
            print(json.dumps(specific_metadata, indent=4))
