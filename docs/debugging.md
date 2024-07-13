# Debugging

## Overview

Debugging the Ansible Dynamic Inventory Script can be done by adjusting logging settings and running the script directly to view output messages. This document provides details on how to configure logging and debug effectively.

## Configuring Logging

The logging configuration, including file paths and log formats, can be customized in the plugin configuration file. For more details, refer to the [Logging section](./plugin-configuration.md#logging) in the plugin configuration documentation.

### Adjusting Log Levels

To enable detailed logging for debugging purposes, you can adjust the `MIN_LOG_LEVEL` in the `xo_inventory.yaml` configuration file.

Example configuration:
```yaml
logging:
  MIN_LOG_LEVEL: DEBUG
```

You can also set the log level to `VERBOSE` for even more detailed output.

### Running the Script Directly

Running the inventory script directly without any arguments will produce log files via standard output (stdout). This can help you evaluate the contents and view debugging messages.

```sh
./inventory.py
```

## Viewing Log Files

Log files are generated based on the configuration settings in the `xo_inventory.yaml` file. Ensure that the `LOG_FILE_PATH` and related settings are correctly configured to store log files in the desired location.

Example configuration:
```yaml
logging:
  LOG_FILE_PATH: '/var/log/ansible-inventory-loader.log'
  ENABLE_FILE_LOGGING: True
  LOG_FILE_MAX_SIZE: 10485760  # 10 MB
  LOG_FILE_BACKUP_COUNT: 3
```

## Example Configuration for Debugging

Here is an example snippet from the `xo_inventory.yaml` configuration file with debugging enabled:

```yaml
logging:
  MIN_LOG_LEVEL: DEBUG
  LOG_FORMAT: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  LOG_TIMESTAMP_FORMAT: '%Y-%m-%dT%H:%M:%S'
  ENABLE_FILE_LOGGING: True
  LOG_FILE_PATH: '/var/log/ansible-inventory-loader.log'
  LOG_FILE_MAX_SIZE: 10485760  # 10 MB
  LOG_FILE_BACKUP_COUNT: 3
```