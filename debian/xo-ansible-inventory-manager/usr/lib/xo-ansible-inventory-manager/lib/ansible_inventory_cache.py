import os
import json
from datetime import datetime
from globals import CACHE_LOCATION
from ansible_inventory_logger import logger

class AnsibleInventoryCache:
    """
    A class responsible for handling the caching of Ansible inventory data.
    """

    @staticmethod
    def is_cache_valid() -> bool:
        """
        Check if the cache file is valid based on its modification time.

        Returns:
            bool: True if the cache is valid (i.e., cache file exists and is newer than the inventory script),
                  False otherwise.
        """
        logger.debug("Checking if cache is valid.")
        if not os.path.exists(CACHE_LOCATION):
            logger.debug("Cache file does not exist.")
            return False

        cache_mtime = datetime.fromtimestamp(os.path.getmtime(CACHE_LOCATION))
        inventory_mtime = datetime.fromtimestamp(os.path.getmtime(__file__))
        is_valid = cache_mtime >= inventory_mtime
        logger.debug(f"Cache is {'valid' if is_valid else 'invalid'} (cache_mtime: {cache_mtime}, inventory_mtime: {inventory_mtime}).")
        return is_valid

    @staticmethod
    def load_cache() -> dict:
        """
        Load the inventory data from the cache file.

        Returns:
            dict: The cached inventory data.
        """
        logger.debug("Loading inventory from cache.")
        with open(CACHE_LOCATION, 'r') as cache_file:
            cache_data = json.load(cache_file)
        logger.debug("Inventory loaded from cache successfully.")
        return cache_data

    @staticmethod
    def save_cache(inventory: dict) -> None:
        """
        Save the inventory data to the cache file.

        Args:
            inventory (dict): The inventory data to cache.

        Returns:
            None
        """
        logger.debug("Saving inventory to cache.")
        with open(CACHE_LOCATION, 'w') as cache_file:
            json.dump(inventory, cache_file)
        logger.debug("Inventory saved to cache successfully.")
