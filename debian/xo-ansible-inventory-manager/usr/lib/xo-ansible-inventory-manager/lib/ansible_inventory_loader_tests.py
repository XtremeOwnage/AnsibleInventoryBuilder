import unittest
import os
import json
import tempfile
import yaml
from ansible_inventory_loader import AnsibleInventoryLoader
from globals import KEY_ENABLED, KEY_ALL
class TestAnsibleInventoryLoader(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the inventory
        self.temp_dir = tempfile.TemporaryDirectory()
        self.loader = AnsibleInventoryLoader(self.temp_dir.name)
        
        # Create mock inventory structure
        self.vars_dir = os.path.join(self.temp_dir.name, 'vars')
        os.makedirs(self.vars_dir, exist_ok=True)
        
        # Create a sample YAML file
        self.sample_yaml = {
            KEY_ENABLED: True,
            'var1': 'value1',
            'var2': 'value2'
        }
        
        self.sample_yaml_disabled = {
            KEY_ENABLED: False,
            'var3': 'value3'
        }

        with open(os.path.join(self.vars_dir, f'{KEY_ALL}.yaml'), 'w') as f:
            yaml.dump(self.sample_yaml, f)
        
        with open(os.path.join(self.vars_dir, 'specific.yml'), 'w') as f:
            yaml.dump(self.sample_yaml, f)
        
        with open(os.path.join(self.vars_dir, 'disabled.yaml'), 'w') as f:
            yaml.dump(self.sample_yaml_disabled, f)
        
    def tearDown(self):
        # Clean up the temporary directory
        self.temp_dir.cleanup()

    def test_should_include_yaml_data(self):
        test_cases = [
            (self.sample_yaml, True),
            (self.sample_yaml_disabled, False),
            ({'some_data': 'value'}, True),
            ({'enabled': False}, False),
            ({'enabled': True}, True)
        ]

        for yaml_data, expected in test_cases:
            with self.subTest(yaml_data=yaml_data):
                result = self.loader.should_include_yaml_data(yaml_data)
                self.assertEqual(result, expected)
    # fix me...
    # def test_load_inventory_data(self):
    #     test_cases = [
    #         ('vars', {
    #             KEY_ENABLED: True, 
    #             'var1': 'value1', 
    #             'var2': 'value2', 
    #             'specific': {
    #                 KEY_ENABLED: True, 
    #                 'var1': 'value1', 
    #                 'var2': 'value2'
    #             }
    #         }),
    #     ]

    #     for subdir, expected in test_cases:
    #         with self.subTest(subdir=subdir):
    #             result = self.loader.load_inventory_data(subdir)
    #             # Convert both dictionaries to JSON strings for comparison
    #             result_json = json.dumps(result, sort_keys=True)
    #             expected_json = json.dumps(expected, sort_keys=True)
    #             self.assertEqual(result_json, expected_json)



    def test_load_inventory_data_with_disabled(self):
        os.makedirs(os.path.join(self.temp_dir.name, 'mixed_vars'), exist_ok=True)
        with open(os.path.join(self.temp_dir.name, 'mixed_vars', 'enabled.yaml'), 'w') as f:
            yaml.dump(self.sample_yaml, f)
        with open(os.path.join(self.temp_dir.name, 'mixed_vars', 'disabled.yaml'), 'w') as f:
            yaml.dump(self.sample_yaml_disabled, f)

        result = self.loader.load_inventory_data('mixed_vars')
        self.assertIn('enabled', result)
        self.assertNotIn('disabled', result)

if __name__ == '__main__':
    unittest.main()
