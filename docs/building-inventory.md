# Ansible Inventory Structure and Organization

## Overview
This document provides detailed information about building, structuring, and organizing the Ansible inventory. It explains the directory structure, rules for defining groups and hosts, and how to use folder structures under `groups`.

## Inventory Path
The inventory path is defined by the `STORAGE_LOCATION` in the plugin's configuration. For more details, refer to the [plugin configuration documentation](./plugin-configuration.md).

## Inventory Directory Structure

The inventory directory may contain three subdirectories: `hosts`, `groups`, and `vars`. Each subdirectory will hold YAML files defining the variables for hosts, groups, and general variables, respectively.

- **`hosts`**: Contains YAML files where each file represents a host.
- **`groups`**: Contains YAML files where each file OR folder represents a group.
- **`vars`**: Contains YAML files with variables that will be automatically merged with the `all` group. This allows better organization of vars based on purpose.

## Example Directory Structure

```
inventory/
├── hosts/                                        # Top-level folder for host variable files
│   ├── host1.yaml                                # Creates host1 and sets its variables
│   ├── host2.yaml                                # Creates host2 and sets its variables
│   └── all.yaml                                  # Variables applied to all hosts, merged with groups/all.yaml
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

## Rules

### Group Rules

- **Default Nesting**: Any group without a parent will automatically be nested as a child of the `all` group.
- **Ungrouped Hosts**: Any host that does not belong to any group will be automatically added to a group named `ungrouped`.
- **Defining Groups**:
  - **YAML File**: Groups can be defined using a `{group-name}.yaml` file under `groups/`. The name of the file (without the extension) will become the group's name.
  - **Folder Structure**: Groups can also be defined using a folder structure under `groups/`. The folder's name will be the group's name. Within this folder, you can add `hosts/`, `vars/`, and `groups/` subfolders to add hosts, variables, and child groups respectively.

### Host Rules

- **Merging Variables**: If a host is defined inside multiple groups, all of the variables will be merged together in the resulting inventory. In the case of duplicate variables, the last file loaded wins.
- **Hosts Definition**: Hosts can be defined in the top-level `hosts/` folder or within `hosts/` subfolders under any group.

### Variable Rules

- **Global Variables**: Variables in `hosts/all.yaml` and `vars/` are automatically merged with `groups/all.yaml` and applied to all hosts and groups.
- **Specific Variables**: Variables defined within a group's `vars/` folder are applied only to that specific group.

## Host Variables (`hosts`)

Each host's YAML file should define the variables for that host. An example `host1.yaml`:

```yaml
enabled: true
ansible_host: 192.168.1.1
type: webserver
```

## Group Variables (`groups`)

Each group's YAML file should define the variables and criteria for that group. An example `group1.yaml`:

```yaml
enabled: true
group_criteria: "type=webserver"
var1: value1
var2: value2
```

## Vars (`vars`)

Any variables defined in the `vars` folder will be automatically merged with the `groups/all` group. This can be used to separate variable files to separate functionality. An example `dns.yaml`:

```yaml
dns_servers:
  - 8.8.8.8
  - 8.8.4.4
```

## Special Groups and Hosts

### All Group

- **Purpose**: The `all` group is a special group where variables defined within it are applied to all hosts and groups.
- **Usage**: Any variables in the `groups/all.yaml` file or in the `vars/` directory are automatically merged into the `all` group, making them globally available to every host and group in the inventory.

### All Host

- **Purpose**: The `all` host is a special host where variables defined within it are merged into every other host, provided the variable was not already defined in that host.
- **Usage**: The `hosts/all.yaml` file contains variables that are automatically merged with variables from other host files. This ensures that common variables, such as global configuration settings, are consistently applied across all hosts unless overridden.

## Nesting Groups, Hosts, and Variables Using Criteria

This plugin allows dynamically nesting objects using expressions. The expression syntax is detailed in the [expression syntax documentation](./expression-syntax.md).

### Group YAML File

Inside a group's `.yaml` file, the following key is valid:

- **`host_criteria`**: Defines an expression. Any hosts matching this expression will automatically be added to this group.

Example `group1.yaml`:

```yaml
enabled: true
host_criteria: "type=webserver"
var1: value1
var2: value2
```

### Group Folder

When using folder structure for creating groups, the `host_criteria` key should be stored in a `_criteria.yaml` file within the group's folder.

Example structure:

```
inventory/
└── groups/
    └── rke/
        ├── _criteria.yaml                    # Defines the criteria for the 'rke' group
        └── groups/
            └── sub-group/
                └── _criteria.yaml            # Defines the criteria for the 'sub-group'
```

### Example `_criteria.yaml`

```yaml
host_criteria: "app=proxmox && type=bare-metal"
```

## Customization

### Customizing Folder Names

The folder names (`hosts`, `groups`, and `vars`) can be customized within the plugin configuration. For more details, refer to the [Configuration/Directories](./plugin-configuration.md#directories) in the plugin configuration documentation.

### Customizing File Extensions

The file extensions for the inventory files are also customizable. By default, the inventory supports `.yml` and `.yaml` extensions, but you can configure additional extensions if needed in the [Configuration/Directories Configuration](./plugin-configuration.md#directories). Note- the file's content must still be YAML!

### Customizing Keys

All keys, and special file-names are also customizable in the [Configuration/Keys](./plugin-configuration.md#directories) section of this plugin's configuration documentation.
