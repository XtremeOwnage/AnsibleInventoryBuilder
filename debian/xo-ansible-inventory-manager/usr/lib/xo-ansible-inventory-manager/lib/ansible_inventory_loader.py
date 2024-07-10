import os
import yaml

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

    def load_inventory_data(self, subdir):
        """
        Load inventory data from YAML files within a specified subdirectory under the main inventory directory.
        This method filters files based on predefined YAML extensions and checks if they should be included 
        based on the 'enabled' flag.
        
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
                name = filename.split('.')[0]  # Remove file extension to get the base name
                file_path = os.path.join(data_dir, filename)
                logger.debug(f"Processing file: {file_path}")

                try:
                    with open(file_path, 'r') as file:
                        yaml_data = yaml.safe_load(file)
                        logger.debug(f"Loaded YAML data: {yaml_data}")
                        
                        # Check if data should be included based on 'enabled' flag
                        if self.should_include_yaml_data(yaml_data):
                            # Merge data under the base filename key, update existing keys with new values
                            data.setdefault(name, {}).update(yaml_data)
                            logger.info(f"Included YAML data for {name}: {yaml_data}")
                        else:
                            logger.info(f"Excluded YAML data for {name}: {yaml_data}")
                except Exception as e:
                    logger.error(f"Failed to load YAML data from file {file_path}: {e}")

        return data
