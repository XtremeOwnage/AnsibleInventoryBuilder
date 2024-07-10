from globals import *  # There are a lot of flags used in this file...
from ansible_inventory_loader import AnsibleInventoryLoader
from ansible_inventory_utils import evaluate_group_criteria
from ansible_inventory_logger import logger

def build_inventory(INVENTORY_DIR):
    """
    Constructs the dynamic inventory for Ansible, using the provided inventory directory.
    
    Args:
        INVENTORY_DIR (str): The path to the directory where inventory data is stored.

    Returns:
        dict: A dictionary representing the Ansible inventory with groups, hosts, and their variables.
    """
    logger.debug("Initializing inventory loading.")
    loader = AnsibleInventoryLoader(INVENTORY_DIR)

    # Load Host Vars, and Group Vars.
    logger.debug("Loading inventory data from files.")
    host_vars_data = loader.load_inventory_data(HOST_VARS_FOLDER)
    group_vars_data = loader.load_inventory_data(GROUP_VARS_FOLDER)

    # Initialize the inventory dictionary
    inventory = {KEY_META: {KEY_HOST_VARS: {}}}

    # Populate the hostvars with the data from host_vars_data, excluding the host defined by KEY_ALL
    logger.debug(f"Merging host and {KEY_HOST_VARS} into [{KEY_META}][{KEY_HOST_VARS}][#]")
    for host, vars in host_vars_data.items():
        if host != KEY_ALL:  # If the host is named 'all', ignore it for now
            inventory[KEY_META][KEY_HOST_VARS][host] = vars  # Add the host, and set its vars

    # Initialize groups based on group_vars_data and add to inventory
    logger.debug("Merging group and group_vars into inventory.")
    for group_name, vars in group_vars_data.items():
        inventory[group_name] = {
            KEY_HOSTS: [],  # Will be filled by evaluate_group_criteria
            KEY_VARS: vars,
            KEY_CHILDREN: []
        }

    # If HOST_VARS_FOLDER/KEY_ALL.yaml exists, we will merge its values with every other host, with an extremely low priority.
    if MERGE_HOST_ALL_VARS:
        all_vars = host_vars_data.get(KEY_ALL, {})
        if all_vars:
            logger.debug(f"Merging variables from {HOST_VARS_FOLDER}/{KEY_ALL} with all hosts.")
            for host, vars in inventory[KEY_META][KEY_HOST_VARS].items():
                for key, value in all_vars.items():
                    # Only set if the host doesn't already have a specific override
                    vars.setdefault(key, value)

    # Evaluate criteria to assign hosts to groups dynamically, based on expressions.
    if EVALUATE_GROUP_CRITERIA:
        logger.debug("Evaluating group criteria for dynamic host assignment.")
        evaluate_group_criteria(inventory, host_vars_data, group_vars_data, HOST_CRITERIA_VAR)

    # Sort inventory for aesthetic purposes if sorting is enabled
    if SORT_ENABLED:
        logger.debug("Sorting the inventory for better readability.")
        inventory = sort_inventory(inventory)
        
    return inventory


def sort_inventory(inventory):
    """
    Sorts various parts of the Ansible inventory based on predefined flags in globals.py.
    This sorting is purely aesthetic, enhancing readability of the inventory output.

    Args:
        inventory (dict): The inventory dictionary to be sorted.
    
    Returns:
        dict: The sorted inventory dictionary.
    """
    logger.info("Starting inventory sorting process.")
    
    if not SORT_ENABLED:
        logger.info("Sorting is disabled. Returning unsorted inventory.")
        return inventory  # Skip sorting if disabled

    # Sorting for groups
    if SORT_GROUP_KEYS:
        logger.debug("Sorting group keys at the root level of the inventory.")
        # Sort the root keys of the inventory, excluding KEY_META to maintain its position
        sorted_keys = sorted(k for k in inventory.keys() if k != KEY_META)
        new_inventory = {k: inventory[k] for k in sorted_keys}
        new_inventory[KEY_META] = inventory[KEY_META]  # Reinsert KEY_META at its original position
        inventory = new_inventory

    if SORT_GROUP_VARS or SORT_GROUP_HOSTS or SORT_GROUP_CHILDREN:
        # Iterate through each group to sort its components
        for group, group_data in inventory.items():
            if group == KEY_META:
                continue  # Skip KEY_META as it's handled separately
            
            if SORT_GROUP_VARS and KEY_VARS in group_data:
                logger.debug(f"Sorting variables within group: {group}")
                group_data[KEY_VARS] = dict(sorted(group_data[KEY_VARS].items()))
            
            if SORT_GROUP_HOSTS and KEY_HOSTS in group_data:
                logger.debug(f"Sorting hosts within group: {group}")
                group_data[KEY_HOSTS] = sorted(group_data[KEY_HOSTS])
            
            if SORT_GROUP_CHILDREN and KEY_CHILDREN in group_data:
                logger.debug(f"Sorting child groups within group: {group}")
                group_data[KEY_CHILDREN] = sorted(group_data[KEY_CHILDREN])

    # Sorting for hostvars
    if SORT_HOSTVAR_KEYS:
        logger.debug("Sorting host keys under KEY_META.")
        inventory[KEY_META][KEY_HOST_VARS] = dict(sorted(inventory[KEY_META][KEY_HOST_VARS].items()))

    # Additional sorting within each host's variables if enabled
    if SORT_HOSTVAR_VARS:
        logger.debug("Sorting variables for each host under KEY_META.")
        for host, host_data in inventory[KEY_META][KEY_HOST_VARS].items():
            if KEY_VARS in host_data:
                host_data[KEY_VARS] = dict(sorted(host_data[KEY_VARS].items()))

    logger.info("Inventory sorting complete.")
    return inventory
