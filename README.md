# Ansible Dynamic Inventory Script

## Overview

This project provides a dynamic inventory script for Ansible, allowing for more flexible and automated management of your infrastructure. The script dynamically constructs an inventory based on host and group variables, along with custom criteria for group membership.

## Features

- **Dynamic Inventory Generation**: Automatically generate inventory from structured YAML files.
- **Group Criteria Evaluation**: Dynamically assign hosts to groups based on custom criteria.
- **Sorting and Organization**: Optional sorting of inventory for improved readability.
- **Comprehensive Logging**: Detailed logging with customizable log levels and formats.

## Configuration

### Inventory Directory Structure

The inventory directory should contain two subdirectories: `host_vars` and `group_vars`. Each subdirectory will hold YAML files defining the variables for hosts and groups, respectively.

- **`host_vars`**: Contains YAML files where each file represents a host.
- **`group_vars`**: Contains YAML files where each file represents a group.

### Example Directory Structure

```
inventory/
├── host_vars/
│   ├── host1.yaml
│   ├── host2.yaml
│   └── all.yaml
├── group_vars/
│   ├── group1.yaml
│   ├── group2.yaml
│   └── all.yaml
├── inventory.py
└── lib/
    ├── ansible_inventory_builder.py
    ├── ansible_inventory_loader.py
    ├── ansible_inventory_logger.py
    ├── ansible_inventory_utils.py
    └── criteria_tokenizer.py
```

### Host Variables (`host_vars`)

Each host's YAML file should define the variables for that host. An example `host1.yaml`:

```yaml
enabled: true
ansible_host: 192.168.1.1
type: webserver
```

### Group Variables (`group_vars`)

Each group's YAML file should define the variables and criteria for that group. An example `group1.yaml`:

```yaml
enabled: true
group_criteria: "type=webserver"
var1: value1
var2: value2
```

## Usage

### Running the Inventory Script

The inventory script should be run with the `--list` or `--host <hostname>` arguments.

- **List all inventory**: `./inventory.py --list`
- **List variables for a specific host**: `./inventory.py --host <hostname>`

### Common Configurations

#### Enable/Disable Debugging

Debugging can be enabled or disabled through the `globals.py` file.

```python
# Enable or disable all debugging
DEBUG_ENABLED = True

# Individual debugging flags
DEBUG_TOKENIZER = False
DEBUG_EVALUATOR = False
DEBUG_EVALUATOR_CONDITIONS = False
DEBUG_EVALUATOR_SHUNTING_YARD = False
DEBUG_INVENTORY = True
```

#### Sorting Configuration

Control sorting through the `globals.py` file.

```python
SORT_ENABLED = True
SORT_GROUP_KEYS = True
SORT_HOSTVAR_KEYS = True
SORT_HOSTVAR_VARS = True
SORT_GROUP_VARS = True
SORT_GROUP_HOSTS = True
SORT_GROUP_CHILDREN = True
```

#### Logging Configuration

Logging configuration is also managed in `globals.py`.

```python
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
CUSTOM_LOG_FORMAT = '{module} {method}: {message}'
LOG_TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S'
ENABLE_FILE_LOGGING = True
LOG_FILE_PATH = '/var/log/ansible-inventory.log'
LOG_FILE_MAX_SIZE = 1024 * 1024 * 5  # 5 MB
LOG_FILE_BACKUP_COUNT = 3
ENABLE_LOG_ROTATION = True
EXIT_ON_ERROR = False
EXIT_ON_FATAL = True
```

## Code Structure

### Criteria Evaluation Language

The criteria language allows for complex expressions to determine group membership.

- **Variables**: Represented by alphanumeric strings.
- **Constants**: Quoted strings or numeric values.
- **Operators**: Include `=`, `!=`, `<`, `<=`, `>`, `>=`, `AND`, `OR`, and more.

### Tokenization

Tokens are extracted from criteria expressions using the `CriteriaTokenizer` class. Each token can be a variable, constant, or operator.

### Group Criteria Evaluation

The `evaluate_group_criteria` function dynamically assigns hosts to groups based on the criteria defined in the group variables. This uses a Shunting Yard algorithm to parse and evaluate the expressions.

## Example

Here is a complete example to demonstrate how everything fits together.

### Directory Structure

```
inventory/
├── host_vars/
│   ├── web1.yaml
│   ├── db1.yaml
│   └── all.yaml
├── group_vars/
│   ├── webservers.yaml
│   ├── databases.yaml
│   └── all.yaml
└── inventory.py
```

### Example Host Variables (`host_vars`)

**`web1.yaml`**:

```yaml
enabled: true
ansible_host: 192.168.1.10
type: webserver
```

**`db1.yaml`**:

```yaml
enabled: true
ansible_host: 192.168.1.20
type: database
```

**`all.yaml`**:

```yaml
enabled: true
ntp_server: time.example.com
```

### Example Group Variables (`group_vars`)

**`webservers.yaml`**:

```yaml
enabled: true
group_criteria: "type=webserver"
var1: value1
```

**`databases.yaml`**:

```yaml
enabled: true
group_criteria: "type=database"
var2: value2
```

**`all.yaml`**:

```yaml
enabled: true
common_var: common_value
```

### Running the Script

To generate the inventory, you can run:

```sh
./inventory.py --list
```

This will output a JSON structure of the inventory based on the host and group variables defined.

### Debugging

If you need to debug the script, you can enable debugging in `globals.py`:

```python
DEBUG_ENABLED = True
DEBUG_INVENTORY = True
```

Then, run the script and observe the debug output to understand how the inventory is being constructed.

### Custom Criteria Evaluation

The criteria evaluation allows for complex expressions. Here are some examples:

- **Simple Criteria**: `type=webserver`
- **Logical AND**: `type=webserver AND environment=production`
- **Logical OR**: `type=webserver OR type=database`
- **Comparison**: `version>=2.0`

These expressions can be used in the `group_vars` files to dynamically assign hosts to groups based on the host variables.

## Conclusion

This project provides a powerful and flexible way to manage Ansible inventories dynamically. By leveraging structured YAML files and custom criteria, you can automate and streamline your infrastructure management with ease. The comprehensive logging and optional sorting further enhance the usability and readability of the generated inventory.
