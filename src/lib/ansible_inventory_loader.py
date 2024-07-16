import os
import yaml

from utils import merge_data
from globals import LOADER_YAML_EXTENSIONS, KEY_ENABLED
from ansible_inventory_logger import logger

class AnsibleInventoryLoader:
    """
    A class responsible for loading inventory data from YAML files located within specified directories.
    This class is specifically designed to handle host and group variable files for an Ansible inventory.
    
    Attributes:
        inventory_dir (str): The base directory path where the inventory data (host_vars and group_vars) is located.
    """

    def __init__(self, inventory_dir):
        """
        Initialize the AnsibleInventoryLoader with the directory where inventory data is located.
        
        Args:
            inventory_dir (str): The directory path containing host_vars and group_vars.
        """
        self.inventory_dir = inventory_dir
        logger.debug(f"Initialized AnsibleInventoryLoader with inventory directory: {inventory_dir}")

    def should_include_yaml_data(self, yaml_data):
        """
        Determine if YAML data should be included in the inventory based on the 'enabled' flag within the data.
        If 'enabled' is set to False, the data will be excluded. By default, data is included.
        
        Args:
            yaml_data (dict): A dictionary containing YAML-loaded data.
        
        Returns:
            bool: True if the YAML data should be included, False otherwise.
        """
        include = yaml_data.get(KEY_ENABLED, True) is not False
        logger.debug(f"YAML data inclusion check - enabled: {include}, data: {yaml_data}")
        return include

    def load_file_data(self, file_path: str) -> dict:
        """
        Load YAML data from a single file. Returns a dictionary with the file's base name (minus extension) as the key.

        Args:
            file_path (str): The path to the YAML file.

        Returns:
            dict: A dictionary containing the base file name as the key and the loaded YAML data as the value.
        """
        try:
            name = os.path.basename(file_path).split('.')[0]  # Get base name without extension
            with open(file_path, 'r') as file:
                yaml_data = yaml.safe_load(file)
                logger.debug(f"Loaded YAML data from {file_path}: {yaml_data}")

                # Check if data should be included based on 'enabled' flag
                if self.should_include_yaml_data(yaml_data):
                    return {name: yaml_data}
                else:
                    logger.info(f"Excluded YAML data from {file_path}")
                    return {}
        except Exception as e:
            logger.error(f"Failed to load YAML data from file {file_path}: {e}")
            return {}

        
    def load_inventory_folder(self, subdir: str) -> dict:
        """
        Load inventory data from YAML files within a specified subdirectory under the main inventory directory.
        This method filters files based on predefined YAML extensions and checks if they should be included 
        based on the 'enabled' flag. This method is not recursive and only processes files in the current directory.

        Args:
            subdir (str): The subdirectory name (usually 'host_vars' or 'group_vars') where the YAML files are located.

        Returns:
            dict: A dictionary containing all the loaded and enabled YAML data, structured by the base name of the files.
        """
        data = {}
        data_dir = os.path.join(self.inventory_dir, subdir)
        logger.info(f"Loading inventory data from directory: {data_dir}")

        # Load YAML files that match the predefined file extensions
        for filename in os.listdir(data_dir):
            if any(filename.endswith(ext) for ext in LOADER_YAML_EXTENSIONS):
                file_data = self.load_file_data(os.path.join(data_dir, filename))
                if file_data:
                    for key, value in file_data.items():
                        if key in data:
                            data[key] = merge_data(data[key], value)
                        else:
                            data[key] = value

        return data


    def load_hosts(self, hosts_folder: str) -> dict[str, dict]:
        """
        Load host data from YAML files within the specified hosts folder.
        This method handles both direct YAML files and nested folders containing host variables.

        Args:
            hosts_folder (str): The path to the hosts folder.

        Returns:
            dict: A dictionary containing all the loaded and enabled host data, structured by the host names.
        """
        hosts_data = {}
        logger.info(f"Loading host data from directory: {hosts_folder}")

        # Process files directly under the hosts_folder
        for entry in os.listdir(hosts_folder):
            entry_path = os.path.join(hosts_folder, entry)

            if os.path.isfile(entry_path) and any(entry.endswith(ext) for ext in LOADER_YAML_EXTENSIONS):
                host_name = entry.split('.')[0]
                logger.debug(f"Processing host file: {entry_path} for host: {host_name}")
                file_data = self.load_inventory_folder(hosts_folder)
                if file_data:
                    hosts_data[host_name] = merge_data(hosts_data.get(host_name, {}), file_data.get(host_name, {}))
                    logger.info(f"Loaded host data for {host_name}: {hosts_data[host_name]}")

            elif os.path.isdir(entry_path):
                host_name = entry
                logger.debug(f"Processing host directory: {entry_path} for host: {host_name}")
                nested_data = self.load_inventory_folder(entry_path)
                if nested_data:
                    hosts_data[host_name] = merge_data(hosts_data.get(host_name, {}), nested_data.get(host_name, {}))
                    logger.info(f"Loaded host data for {host_name}: {hosts_data[host_name]}")

        logger.info(f"Completed loading host data from {hosts_folder}")
        return hosts_data

    def load_groups(self, groups_folder: str, parent_group: str = None) -> dict[str, dict]:
        """
        Load group data from YAML files and folders within the specified groups folder.
        This method handles both direct YAML files, nested groups, hosts folders, and vars folders.

        Args:
            groups_folder (str): The path to the groups folder.
            parent_group (str): The name of the parent group, if this method is called recursively.

        Returns:
            dict: A dictionary containing all the loaded and enabled group data, structured by the group names.
        """
        groups_data = {}
        logger.info(f"Loading group data from directory: {groups_folder}")

        for entry in os.listdir(groups_folder):
            entry_path = os.path.join(groups_folder, entry)

            if os.path.isfile(entry_path) and any(entry.endswith(ext) for ext in LOADER_YAML_EXTENSIONS):
                group_name = entry.split('.')[0]
                logger.debug(f"Processing group file: {entry_path} for group: {group_name}")
                file_data = self.load_inventory_folder(groups_folder)
                if file_data:
                    groups_data[group_name] = merge_data(groups_data.get(group_name, {KEY_HOSTS: [], KEY_VARS: {}, KEY_CHILDREN: []}), file_data.get(group_name, {}))
                    logger.info(f"Loaded group data for {group_name}: {groups_data[group_name]}")

            elif os.path.isdir(entry_path):
                group_name = entry
                logger.debug(f"Processing group directory: {entry_path} for group: {group_name}")
                groups_data[group_name] = groups_data.get(group_name, {KEY_HOSTS: [], KEY_VARS: {}, KEY_CHILDREN: []})

                for sub_entry in os.listdir(entry_path):
                    sub_entry_path = os.path.join(entry_path, sub_entry)

                    if os.path.isdir(sub_entry_path):
                        if sub_entry == 'hosts':
                            logger.debug(f"Processing hosts folder: {sub_entry_path} for group: {group_name}")
                            hosts_data = self.load_hosts(sub_entry_path)
                            groups_data[group_name][KEY_HOSTS].extend(hosts_data.keys())
                            logger.info(f"Added hosts for group {group_name}: {hosts_data.keys()}")

                        elif sub_entry == 'vars':
                            logger.debug(f"Processing vars folder: {sub_entry_path} for group: {group_name}")
                            vars_data = self.load_inventory_folder(sub_entry_path)
                            groups_data[group_name][KEY_VARS] = merge_data(groups_data[group_name][KEY_VARS], vars_data)
                            logger.info(f"Updated vars for group {group_name} with data from vars folder")

                        elif sub_entry == 'groups':
                            logger.debug(f"Processing child groups folder: {sub_entry_path} for group: {group_name}")
                            child_groups_data = self.load_groups(sub_entry_path, group_name)
                            groups_data[group_name][KEY_CHILDREN].extend(child_groups_data.keys())
                            groups_data.update(child_groups_data)
                            logger.info(f"Added child groups for group {group_name}: {child_groups_data.keys()}")

                    elif os.path.isfile(sub_entry_path) and sub_entry == GROUP_CRITERIA_FILE:
                        logger.debug(f"Processing criteria file: {sub_entry_path} for group: {group_name}")
                        criteria_data = self.load_inventory_folder(entry_path)
                        if criteria_data:
                            groups_data[group_name][KEY_VARS].update(criteria_data.get(group_name, {}))
                            logger.info(f"Loaded criteria data for {group_name}: {groups_data[group_name]}")

                if parent_group:
                    groups_data[parent_group][KEY_CHILDREN].append(group_name)
                    logger.info(f"Added group {group_name} as child of {parent_group}")

        logger.info(f"Completed loading group data from {groups_folder}")
        return groups_data
