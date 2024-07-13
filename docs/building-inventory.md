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