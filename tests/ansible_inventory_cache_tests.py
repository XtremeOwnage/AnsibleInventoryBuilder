import unittest
from unittest.mock import patch, mock_open
from datetime import datetime
from ansible_inventory_cache import AnsibleInventoryCache

class TestAnsibleInventoryCache(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('ansible_inventory_logger.logger.debug')
    def test_is_cache_valid(self, mock_logger, mock_getmtime, mock_exists):
        # Test case where cache does not exist
        mock_exists.return_value = False
        self.assertFalse(AnsibleInventoryCache.is_cache_valid())
        mock_logger.assert_called_with("Cache file does not exist.")
        
        # Test case where cache exists but is older than inventory script
        mock_exists.return_value = True
        mock_getmtime.side_effect = [datetime(2021, 1, 1).timestamp(), datetime(2021, 1, 2).timestamp()]
        self.assertFalse(AnsibleInventoryCache.is_cache_valid())
        mock_logger.assert_called_with("Cache is invalid (cache_mtime: 2021-01-01 00:00:00, inventory_mtime: 2021-01-02 00:00:00).")
        
        # Test case where cache is newer than inventory script
        mock_getmtime.side_effect = [datetime(2021, 1, 2).timestamp(), datetime(2021, 1, 1).timestamp()]
        self.assertTrue(AnsibleInventoryCache.is_cache_valid())
        mock_logger.assert_called_with("Cache is valid (cache_mtime: 2021-01-02 00:00:00, inventory_mtime: 2021-01-01 00:00:00).")

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    @patch('ansible_inventory_logger.logger.debug')
    def test_load_cache(self, mock_logger, mock_open):
        expected_data = {"key": "value"}
        cache_data = AnsibleInventoryCache.load_cache()
        self.assertEqual(cache_data, expected_data)
        mock_logger.assert_called_with("Inventory loaded from cache successfully.")

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('ansible_inventory_logger.logger.debug')
    def test_save_cache(self, mock_logger, mock_json_dump, mock_open):
        inventory_data = {"key": "value"}
        AnsibleInventoryCache.save_cache(inventory_data)
        mock_open.assert_called_once_with('/tmp/ansible-inventory-cache.json', 'w')
        mock_json_dump.assert_called_once_with(inventory_data, mock_open())
        mock_logger.assert_called_with("Inventory saved to cache successfully.")

if __name__ == '__main__':
    unittest.main()
