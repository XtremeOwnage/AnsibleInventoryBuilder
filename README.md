Certainly! Here is the complete updated `README.md`:

# Ansible Dynamic Inventory Script

## Overview

This project provides a dynamic inventory script for Ansible, allowing for more flexible and automated management of your infrastructure. The script dynamically constructs an inventory based on host and group variables, along with custom criteria for group membership.

## Features

- **Dynamic Inventory Generation**: Automatically generate inventory from structured YAML files and folders.
- **Group Criteria Evaluation**: Dynamically assign hosts to groups based on custom criteria.
- **Comprehensive Logging**: Detailed logging with customizable log levels and formats.

## Installation

### High-Level Installation (Using dpkg)

1. **Download the Package**: Obtain the `.deb` package from the releases section of this repository.
2. **Install the Package**: Use `dpkg -i` to install the package.
3. **Configure the Plugin**: Edit `/etc/ansible/xo_inventory.yaml` file to configure the plugin settings. [example/xo_inventory.yaml](./example/xo_inventory.yaml)
4. **Update Ansible Configuration**: Modify `/etc/ansible/ansible.cfg` to use the inventory plugin. [example/ansible.cfg](./example/ansible.cfg)

For detailed installation instructions, refer to the [Plugin Installation](./docs/plugin-installation.md) documentation.

## Configuration

The bare minimum configuration requires setting the `STORAGE_LOCATION` to point to your inventory location. 

For detailed configuration options, refer to the [Plugin Configuration](./docs/plugin-configuration.md) documentation.

## Usage

### Running the Inventory Script

The inventory script should be run with the `--list` or `--host <hostname>` arguments.

- **List all inventory**: `./inventory.py --list`
- **List variables for a specific host**: `./inventory.py --host <hostname>`

### Common Configurations

Please see [Plugin Configuration](./docs/plugin-configuration.md).

## Code Structure

### Criteria Evaluation Language

The criteria language allows for complex expressions to determine group membership. For more details, refer to the [Expression Syntax](./docs/expression-syntax.md) documentation.

## Building Inventory

For detailed instructions on building and organizing your inventory, refer to the [Building Inventory](./docs/building-inventory.md) documentation.

## Example Directory Structure

```
inventory/
├── hosts/                                        # Top-level folder for host variable files
│   ├── host1.yaml                                # Creates host1 and sets its variables
│   ├── host2.yaml                                # Creates host2 and sets its variables
├── groups/                                       # Top-level folder for group variable files and sub-groups
│   ├── group1.yaml                               # Creates group1 and sets its variables and criteria
│   ├── group2.yaml                               # Creates group2 and sets its variables and criteria
│   ├── rke/                                      # Folder for the 'rke' group
│   │   ├── _criteria.yaml                        # Defines criteria to automatically add hosts to the 'rke' group
│   │   ├── hosts/                                # Folder for hosts specific to the 'rke' group
│   │   │   ├── host3.yaml                        # Creates host3 under 'rke' and sets its variables
│   │   │   └── host4.yaml                        # Creates host4 under 'rke' and sets its variables
│   │   ├── vars/                                 # Folder for variables specific to the 'rke' group
│   │   │   ├── specific.yaml                     # Specific variables for 'rke'
│   │   │   └── general.yaml                      # General variables for 'rke'
│   │   └── groups/                               # Folder for child groups under 'rke'
│   │       ├── child-group1.yaml                 # Creates child-group1 under 'rke' and sets its variables
│   │       ├── child-group2.yaml                 # Creates child-group2 under 'rke' and sets its variables
│   │       └── sub-group/                        # Sub-folder for further nesting under 'rke'
│   │           ├── _criteria.yaml                # Defines criteria to automatically add hosts to the 'sub-group' group
│   │           ├── hosts/                        # Folder for hosts specific to the sub-group
│   │           │   ├── host5.yaml                # Creates host5 under the sub-group and sets its variables
│   │           │   └── host6.yaml                # Creates host6 under the sub-group and sets its variables
│   │           ├── vars/                         # Folder for variables specific to the sub-group
│   │           │   ├── more-specific.yaml        # More specific variables for the sub-group
│   │           │   └── additional.yaml           # Additional variables for the sub-group
│   │           └── groups/                       # Folder for child groups under the sub-group
│   │               ├── sub-child-group1.yaml     # Creates sub-child-group1 under the sub-group and sets its variables
│   │               └── sub-child-group2.yaml     # Creates sub-child-group2 under the sub-group and sets its variables
│   └── all.yaml                                  # Variables applied to all groups
├── vars/                                         # Top-level folder for general variables
│   ├── dns.yaml                                  # DNS-specific variables, merged with groups/all.yaml
│   └── common.yaml                               # Common variables shared across multiple groups/hosts, merged with groups/all.yaml
```

## Example Host Variables (`hosts`)

**`host1.yaml`**:

```yaml
enabled: true
ansible_host: 192.168.1.1
type: webserver
```

## Example Group Variables (`groups`)

**`group1.yaml`**:

```yaml
enabled: true
host_criteria: "type=webserver"
var1: value1
```

## Example General Variables (`vars`)

**`dns.yaml`**:

```yaml
dns_servers:
  - 8.8.8.8
  - 8.8.4.4
```

**`common.yaml`**:

```yaml
timezone: UTC
backup_retention_days: 7
```

## Custom Criteria Evaluation

The criteria evaluation allows for complex expressions. Here are some examples:

- **Simple Criteria**: `type=webserver`
- **Logical AND**: `type=webserver AND environment=production`
- **Logical OR**: `type=webserver OR type=database`
- **Comparison**: `version>=2.0`

These expressions can be used in the `group_vars` files to dynamically assign hosts to groups based on the host variables. For more details, refer to the [Expression Syntax](./docs/expression-syntax.md) documentation.

## Debugging

For detailed debugging instructions, refer to the [Debugging](./docs/debugging.md) documentation.

## Testing

For detailed testing instructions, refer to the [Testing](./docs/testing.md) documentation.

## Removal / Uninstall

Please refer to [Removing the Plugin](./docs/plugin-installation.md#removing-the-plugin)