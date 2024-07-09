# globals.py
import logging
import yaml
import os

"""
Global configuration settings for debugging levels and directory paths in the inventory management system.
This file organizes settings into various sections, allowing for easy modification and quick reference.
"""

def load_config() -> dict:
    """
    Load the configuration from the YAML file located in one of the predefined paths.
    
    The method checks the following locations in order:
    1. /etc/ansible/inventory_loader.yaml
    2. (Ansible Env Inventory Location)/inventory_loader.yaml
    3. (Current Directory)/inventory_loader.yaml

    Returns:
        dict: The loaded configuration dictionary.

    Raises:
        FileNotFoundError: If no configuration file is found in the predefined locations.
    """
    config_paths = [
        '/etc/ansible/inventory_loader.yaml',
        os.path.join(os.environ.get('ANSIBLE_INVENTORY', ''), 'inventory_loader.yaml'),
        os.path.join(os.path.dirname(__file__), 'inventory_loader.yaml')
    ]

    for path in config_paths:
        if os.path.exists(path):
            with open(path, 'r') as file:
                return yaml.safe_load(file)

    raise FileNotFoundError("No configuration file found in predefined locations.")


# Load the configuration from the YAML file
config = load_config()

####### SECTION: Main Configuration #######
"""
This section contains primary configuration settings for the inventory system.
"""

# Path where inventory-related files are stored.
STORAGE_LOCATION: str = config['main']['STORAGE_LOCATION']
"""
Path where inventory-related files are stored.
Example: /root/Ansible/inventory
"""

####### SECTION: Logging Configuration #######
"""
This section defines customizable logging settings for the inventory system.
Users can modify these settings to control log output formats and behaviors.

Log Formatting:
- LOG_FORMAT: Standard logging format used for configuring how messages are logged to console or files.
  Supported tokens are based on the Python logging library. Detailed info: 
  https://docs.python.org/3/library/logging.html#logrecord-attributes

- CUSTOM_LOG_FORMAT: Custom format for dynamically inserting runtime details such as module and method names into logs.
  This format allows for inserting additional context that helps in tracing logs back to their source more effectively.

Supported Tokens for CUSTOM_LOG_FORMAT:
- {module}: The name of the module where the log call originates.
- {method}: The method or function name where the log call is made.
- {message}: The log message.

Additional Tokens:
- {pathname}: Full pathname of the source file where the logging call was issued.
- {lineno}: Source line number where the logging call was issued.

Time Customization:
- To customize the time format in logs to ISO8601, adjust the LOG_FORMAT string to include time in the desired format.
  Example for ISO8601: '%(asctime)s' with '%Y-%m-%dT%H:%M:%S' as the datefmt in logging setup.

Relationship between LOG_FORMAT and CUSTOM_LOG_FORMAT:
- LOG_FORMAT defines the overall structure of log entries and is applied globally in the logger configuration.
- CUSTOM_LOG_FORMAT is used specifically within the logging calls to format the message part of the log with runtime details.
"""

# Basic format for log messages, defaulting to ISO8601 time format
LOG_FORMAT: str = config['logging']['LOG_FORMAT']
"""
Basic format for log messages, defaulting to ISO8601 time format
"""

LOG_TIMESTAMP_FORMAT: str = config['logging']['LOG_TIMESTAMP_FORMAT']
"""
Timestamp format for log messages, defaulting to ISO8601 format
"""

# Custom format for displaying the module and method in log messages
CUSTOM_LOG_FORMAT: str = config['logging']['CUSTOM_LOG_FORMAT']
"""
Custom format for displaying the module and method in log messages
"""

# Enable or disable log file rotation
ENABLE_LOG_ROTATION: bool = config['logging']['ENABLE_LOG_ROTATION']
"""
Enable or disable log file rotation
"""

# Flag to control whether the application should exit on errors
EXIT_ON_ERROR: bool = config['logging']['EXIT_ON_ERROR']
"""
Flag to control whether the application should exit on errors
"""

# Flag to control whether the application should exit on fatal logs
EXIT_ON_FATAL: bool = config['logging']['EXIT_ON_FATAL']
"""
Flag to control whether the application should exit on fatal logs
"""

# Logging file path
LOG_FILE_PATH: str = config['logging']['LOG_FILE_PATH']
"""
Logging file path
"""

# Enable or disable file logging
ENABLE_FILE_LOGGING: bool = config['logging']['ENABLE_FILE_LOGGING']
"""
Enable or disable file logging
"""

# Log file rotation settings
LOG_FILE_MAX_SIZE: int = config['logging']['LOG_FILE_MAX_SIZE']
"""
Log file rotation settings: maximum size of the log file in bytes
"""

LOG_FILE_BACKUP_COUNT: int = config['logging']['LOG_FILE_BACKUP_COUNT']
"""
Log file rotation settings: number of backup files to keep
"""

# Minimum logging level
MIN_LOG_LEVEL: int = getattr(logging, config['logging']['MIN_LOG_LEVEL'], logging.ERROR)
"""
Minimum logging level
"""

####### SECTION: Debugging Control Flags #######
"""
This section contains flags that enable or disable debugging for various components of the system.
The DEBUG_ENABLED flag acts as a master switch for all debugging output.
"""

# Debugging for the shunting yard algorithm used in parsing expressions
DEBUG_EVALUATOR_SHUNTING_YARD: bool = config['debugging']['DEBUG_EVALUATOR_SHUNTING_YARD']
"""
Debugging for the shunting yard algorithm used in parsing expressions
"""

####### SECTION: Directory and File Configurations #######
"""
This section defines the folder paths and file types that the inventory system will interact with.
These settings are used to locate and load host and group variable files.
"""

# Path to the folder containing host variable files
HOST_VARS_FOLDER: str = config['directories']['HOST_VARS_FOLDER']
"""
Path to the folder containing host variable files
"""

# Path to the folder containing group variable files
GROUP_VARS_FOLDER: str = config['directories']['GROUP_VARS_FOLDER']
"""
Path to the folder containing group variable files
"""

# List of valid YAML file extensions to be considered in loading processes
LOADER_YAML_EXTENSIONS: list = config['directories']['LOADER_YAML_EXTENSIONS']
"""
List of valid YAML file extensions to be considered in loading processes
"""

####### SECTION: Inventory Key Configurations #######
"""
These settings define various key names used in the inventory scripts. 
These include keys for enabling/disabling groups or hosts and special keys for internal logic.
"""

# Key for identifying the group criteria in group vars
HOST_CRITERIA_VAR: str = config['keys']['HOST_CRITERIA_VAR']
"""
Key for identifying the group criteria in group vars
"""

# Key used to enable or disable hosts or groups dynamically
KEY_ENABLED: str = config['keys']['KEY_ENABLED']
"""
Key used to enable or disable hosts or groups dynamically
"""

# Special key indicating the global 'all' group in group vars, and indicating the 'all' host in host-vars.
KEY_ALL: str = config['keys']['KEY_ALL']
"""
Special key indicating the global 'all' group in group vars, and indicating the 'all' host in host-vars.
"""

# Key under which host variables are stored in the output inventory
KEY_HOST_VARS: str = config['keys']['KEY_HOST_VARS']
"""
Key under which host variables are stored in the output inventory
"""

# This is the _meta key, in the root of the inventory which holds... hostvars.
KEY_META: str = config['keys']['KEY_META']
"""
This is the _meta key, in the root of the inventory which holds... hostvars.
"""

# This key is used in both _meta/host_vars/#/vars, as well as #/vars
KEY_VARS: str = config['keys']['KEY_VARS']
"""
This key is used in both _meta/host_vars/#/vars, as well as #/vars
"""

# This key is used under #/hosts, to indicate which hosts belong to a specific group.
KEY_HOSTS: str = config['keys']['KEY_HOSTS']
"""
This key is used under #/hosts, to indicate which hosts belong to a specific group.
"""

# This key is used under #/children, and groups nested under the current group.
KEY_CHILDREN: str = config['keys']['KEY_CHILDREN']
"""
This key is used under #/children, and groups nested under the current group.
"""

####### SECTION: Feature Flags #######
"""
This section contains boolean flags that enable or disable specific features or behaviors within the inventory system.
"""

# Flag to add all detected hosts to the 'all' group automatically
ADD_ALL_HOSTS_TO_ALL_GROUP: bool = config['features']['ADD_ALL_HOSTS_TO_ALL_GROUP']
"""
Flag to add all detected hosts to the 'all' group automatically
"""

# If, there is a HOST_VARS_FOLDER/KEY_ALL.yaml host, aka, a host named, 'all'
# This will merge the vars from that host, into every other host, IF the var was not already defined.
# Aka- this is the lowest priority.
MERGE_HOST_ALL_VARS: bool = config['features']['MERGE_HOST_ALL_VARS']
"""
If, there is a HOST_VARS_FOLDER/KEY_ALL.yaml host, aka, a host named, 'all'
This will merge the vars from that host, into every other host, IF the var was not already defined.
Aka- this is the lowest priority.
"""

# Enables or disables the functionality to evaluate group criteria.
# Given- this is the primary reason this library / inventory script was written- why would you disable it?
EVALUATE_GROUP_CRITERIA: bool = config['features']['EVALUATE_GROUP_CRITERIA']
"""
Enables or disables the functionality to evaluate group criteria.
Given- this is the primary reason this library / inventory script was written- why would you disable it?
"""

####### SECTION: Output Sorting #######
"""
This section contains boolean flags which will enable, or disable the sorting of the output data.
Note- Ansible does not care if the output is sorted. This is all for aesthetic reasons.
There is literally no advantage at all to sorting, other then having happy thoughts from looking at perfectly sorted data.
"""

# This is a "master" flag, which will enable or disable all sorting. If disabled, the other sorting keys have no effect.
SORT_ENABLED: bool = config['sorting']['SORT_ENABLED']
"""
This is a "master" flag, which will enable or disable all sorting. If disabled, the other sorting keys have no effect.
"""

# Will automatically sort group keys based on name.
SORT_GROUP_KEYS: bool = config['sorting']['SORT_GROUP_KEYS']
"""
Will automatically sort group keys based on name.
"""

# Alphabetically sort keys under _meta/host_vars
SORT_HOSTVAR_KEYS: bool = config['sorting']['SORT_HOSTVAR_KEYS']
"""
Alphabetically sort keys under _meta/host_vars
"""

# Alphabetically sort keys under _meta/host_vars/*/vars
SORT_HOSTVAR_VARS: bool = config['sorting']['SORT_HOSTVAR_VARS']
"""
Alphabetically sort keys under _meta/host_vars/*/vars
"""

# Alphabetically sort keys under */vars
SORT_GROUP_VARS: bool = config['sorting']['SORT_GROUP_VARS']
"""
Alphabetically sort keys under */vars
"""

# Alphabetically sort keys under */hosts
SORT_GROUP_HOSTS: bool = config['sorting']['SORT_GROUP_HOSTS']
"""
Alphabetically sort keys under */hosts
"""

# Alphabetically sort keys under */children
SORT_GROUP_CHILDREN: bool = config['sorting']['SORT_GROUP_CHILDREN']
"""
Alphabetically sort keys under */children
"""

####### SECTION: Caching Configuration #######
"""
This section contains configuration settings for enabling and managing the caching of the inventory data.
Caching helps improve performance by storing the generated inventory data and reusing it until the cache is invalidated.
"""

# Enable, or disable file cache.
CACHE_ENABLED: bool = config['cache']['CACHE_ENABLED']
"""
This flag enables or disables the caching feature.
If enabled, the inventory data will be cached to improve performance.
If disabled, the inventory data will be generated

 fresh on each run.
"""

# Output path for cache file.
CACHE_LOCATION: str = config['cache']['CACHE_LOCATION']
"""
This defines the file path where the cache will be stored.
The cache file contains the serialized inventory data.
Ensure the specified path is writable by the script.
"""