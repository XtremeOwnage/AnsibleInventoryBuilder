# Ansible Inventory Configuration Documentation

## Overview
This document provides detailed information about configuring the `xo_inventory.yaml` file for Ansible inventory management. This file is essential for customizing various settings such as logging, debugging, directory paths, keys, features, sorting, and caching.

## Configuration File Location
The configuration file `xo_inventory.yaml` can be loaded from multiple locations with the following order of precedence, where the highest option takes priority:

1. `(Current Directory)/xo_inventory.yaml`
2. `(Ansible Env Inventory Location)/xo_inventory.yaml`
3. `/etc/ansible/xo_inventory.yaml`

For a complete example configuration file, refer to the [Example Config](./../example/xo_inventory.yaml).

## Configuration Sections

### Main
Defines the **primary storage location for inventory-related files**. **You MUST customize this location** to suit your environment.

```yaml
main:
  STORAGE_LOCATION: /home/your-user/Ansible/inventory  
```

> **IMPORTANT**: 
> - **You MUST customize the `STORAGE_LOCATION` to your specific environment.**
> - This path is critical for the proper functioning of your inventory management.
> - Ensure that the directory exists and is accessible by your Ansible processes.

### Logging
Customizable logging settings for the inventory system.
```yaml
logging:
  LOG_FORMAT: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  LOG_TIMESTAMP_FORMAT: '%Y-%m-%dT%H:%M:%S'
  CUSTOM_LOG_FORMAT: "{module} {method}: {message}"
  ENABLE_LOG_ROTATION: True
  EXIT_ON_ERROR: False
  EXIT_ON_FATAL: True
  LOG_FILE_PATH: '/var/log/ansible-inventory-loader.log'
  ENABLE_FILE_LOGGING: True
  LOG_FILE_MAX_SIZE: 10485760  # 10 MB
  LOG_FILE_BACKUP_COUNT: 3
  MIN_LOG_LEVEL: ERROR
```

### Debugging
Flags that enable or disable debugging for various components of the system.
```yaml
debugging:
  DEBUG_EVALUATOR_SHUNTING_YARD: True
```

### Directories
Defines folder paths and file types that the inventory system interacts with.
```yaml
directories:
  HOST_VARS_FOLDER: 'hosts'
  GROUP_VARS_FOLDER: 'groups'
  VARS_FOLDER: 'vars'
  LOADER_YAML_EXTENSIONS: ['.yaml', '.yml']
```

### Keys
Defines various key names used in the inventory scripts.
```yaml
keys:
  HOST_CRITERIA_VAR: 'host_criteria'
  KEY_ENABLED: 'enabled'
  KEY_ALL: 'all'
  KEY_HOST_VARS: 'host_vars'
  KEY_META: '_meta'
  KEY_VARS: 'vars'
  KEY_HOSTS: 'hosts'
  KEY_CHILDREN: 'children'
```

### Features
Flags that enable or disable specific features or behaviors within the inventory system.
```yaml
features:
  ADD_ALL_HOSTS_TO_ALL_GROUP: True
  MERGE_HOST_ALL_VARS: True
  EVALUATE_GROUP_CRITERIA: True
```

### Sorting
Flags to enable or disable the sorting of the output data for aesthetic purposes.
```yaml
sorting:
  SORT_ENABLED: True
  SORT_GROUP_KEYS: True
  SORT_HOSTVAR_KEYS: True
  SORT_HOSTVAR_VARS: True
  SORT_GROUP_VARS: True
  SORT_GROUP_HOSTS: True
  SORT_GROUP_CHILDREN: True
```

### Cache
Configuration settings for enabling and managing the caching of inventory data to improve performance.
```yaml
cache:
  CACHE_ENABLED: True
  CACHE_LOCATION: "/tmp/ansible-inventory-cache.json"
```

## How to Configure

1. **Choose the Configuration File Location:**
   Decide where you want to place your `xo_inventory.yaml` based on the precedence order mentioned above.

2. **Edit the Configuration File:**
   Customize each section of the `xo_inventory.yaml` file according to your requirements. You can refer to the provided example configuration for guidance: [Example Config](./../example/xo_inventory.yaml).

3. **Ensure Proper Permissions:**
   Make sure that the path specified for logs and cache is writable by the script.

4. **Testing Configuration:**
   After configuring the file, test the setup to ensure that all paths and settings are correctly applied and that the inventory system behaves as expected.

## Example Configuration File
For a complete configuration file example, see the [Example Config](./../example/xo_inventory.yaml).