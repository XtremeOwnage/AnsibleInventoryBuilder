#!/usr/bin/python3
import sys
import json
import os
import io
from contextlib import redirect_stdout

from globals import KEY_HOST_VARS, CACHE_ENABLED, STORAGE_LOCATION
from ansible_inventory_cache import AnsibleInventoryCache

# Import the build_inventory function from the ansible_inventory_builder module
from ansible_inventory_builder import build_inventory

def load_inventory() -> dict:
    """
    Load the inventory, either from the cache or by building it anew.

    This method checks if caching is enabled and whether the cache is valid. If so, it loads the inventory from the cache.
    Otherwise, it builds the inventory and saves it to the cache if caching is enabled.

    Args:
        INVENTORY_DIR (str): The path to the directory where inventory data is stored.

    Returns:
        dict: The inventory data.
    """
    # Check cache if enabled
    if CACHE_ENABLED and AnsibleInventoryCache.is_cache_valid():
        inventory = AnsibleInventoryCache.load_cache()
    else:
        # Build the inventory using the INVENTORY_DIR
        inventory = build_inventory(STORAGE_LOCATION)
        # Save to cache if enabled
        if CACHE_ENABLED:
            AnsibleInventoryCache.save_cache(inventory)
    return inventory

def main():
    """
    Main function to handle the execution of the inventory script.

    This function checks the command-line arguments and either lists the full inventory or provides
    host-specific variables. It also handles caching to improve performance.

    Returns:
        None
    """
    # Check if any command-line arguments are passed
    if len(sys.argv) > 1:
        if sys.argv[1] == '--list':
            # Load the inventory
            inventory = load_inventory()
            # Print the inventory
            print(json.dumps(inventory))

        elif sys.argv[1] == '--host':
            # Check if a hostname is provided after the '--host' argument
            hostname = sys.argv[2] if len(sys.argv) > 2 else None
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                if hostname:
                    # Retrieve host variables for the given hostname from the inventory
                    host_vars = load_inventory()['_meta'][KEY_HOST_VARS].get(hostname, {})
                    # Convert the host variables to JSON and print
                    print(json.dumps(host_vars))
                else:
                    # If no hostname is provided, print an empty JSON object
                    print(json.dumps({}))
            # Write the content of the buffer to standard output
            sys.stdout.write(buffer.getvalue())

    else:
        # Default behavior when no arguments are provided
        # Build the inventory and print it with indentation for better readability
        inventory = load_inventory()
        print(json.dumps(inventory, indent=4))

# Check if this script is executed as the main program and not imported as a module
if __name__ == '__main__':
    main()

    ## TO DO - All child groups need to be added to the "all" group under children.
    ## TO DO - Any hosts not in a group besides "ALL" needs to be under
    ## TO DO - All hosts, need to be added to the "all" group, under hosts
    # https://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html
    # https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html