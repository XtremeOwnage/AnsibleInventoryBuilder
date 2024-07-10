from ansible_inventory_logger import logger
from criteria_evaluator import CriteriaEvaluator
from globals import KEY_HOST_VARS, KEY_ALL, KEY_HOSTS, KEY_VARS, KEY_CHILDREN, KEY_META

def add_hosts_to_all_group(inventory):
    """
    Gathers all host names from the hostvars, ensures there are no duplicates,
    sorts them alphabetically, and adds them to the 'all' group in the inventory.

    Args:
        inventory (dict): The inventory dictionary to be updated.

    Returns:
        None: The function directly modifies the 'inventory' dictionary.
    """
    method_name = "add_hosts_to_all_group"
    logger.debug(f"{method_name}: Gathering all hosts for the 'all' group.")

    # Extract all unique host names from the KEY_META section
    all_hosts = set(inventory[KEY_META][KEY_HOST_VARS].keys())

    logger.info(f"{method_name}: Found {len(all_hosts)} unique hosts.")

    # Sort hosts alphabetically and assign to the 'all' group
    inventory[KEY_ALL] = {KEY_HOSTS: sorted(all_hosts), KEY_VARS: {}, KEY_CHILDREN: []}

    logger.debug(f"{method_name}: All hosts have been added to the 'all' group.")

def evaluate_group_criteria(inventory, host_vars_data, group_vars_data, GROUP_CRITERIA_VAR):
    """
    Evaluates and assigns hosts to groups based on criteria specified in the group_vars.

    Args:
        inventory (dict): The inventory dictionary to be updated.
        host_vars_data (dict): Dictionary containing host variables.
        group_vars_data (dict): Dictionary containing group variables.
        GROUP_CRITERIA_VAR (str): The variable name in group_vars that contains criteria for host assignment.

    Returns:
        None: The function directly modifies the 'inventory' dictionary.
    """
    method_name = "evaluate_group_criteria"
    logger.debug(f"{method_name}: Starting group criteria evaluation.")
    
    # Initialize the CriteriaEvaluator with current host and group vars data
    evaluator = CriteriaEvaluator(host_vars_data, group_vars_data, GROUP_CRITERIA_VAR)
    logger.debug(f"{method_name}: CriteriaEvaluator initialized.")

    # Loop through each group and evaluate criteria if defined
    for group_name, group_vars in group_vars_data.items():
        # Ensure group_vars is a dictionary and contains data before evaluating criteria
        if isinstance(group_vars, dict) and group_vars:
            if group_name not in inventory:
                logger.debug(f"{method_name}: Group {group_name} added to inventory.")
                inventory[group_name] = {KEY_HOSTS: [], KEY_VARS: group_vars.copy()}

            if GROUP_CRITERIA_VAR in group_vars:
                criteria = group_vars[GROUP_CRITERIA_VAR]
                for host, details in host_vars_data.items():
                    if evaluator.evaluate_criteria(criteria, host):
                        inventory[group_name][KEY_HOSTS].append(host)
                        logger.debug(f"{method_name}: Host {host} added to group {group_name}.")
    logger.debug(f"{method_name}: Finished group criteria evaluation.")
