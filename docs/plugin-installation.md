# Plugin Installation

## Preferred Installation Method

The preferred method of installation is by using the `.deb` file, which can be downloaded from the repository's releases.

### Steps to Install

1. **Download the Package**: Obtain the `.deb` package from the [releases section](https://github.com/XtremeOwnage/XO-Ansible-Inventory-Manager/releases) of this repository.
2. **Install the Package**: Use `dpkg -i` to install the package.

```sh
sudo dpkg -i xo-ansible-inventory-manager.deb
```

3. **Configure the Plugin**: Edit the configuration file at `/etc/ansible/xo_inventory.yaml` to set the appropriate settings.

## Manual Installation

If you prefer to install manually, follow the steps below. Ensure you have Python installed on your system.

### Manual Installation Script

If you prefer to manually install this plugin, here is a script to do it for you.

```bash
#!/bin/bash
set -e

# Clone the repository
git clone https://github.com/XtremeOwnage/XO-Ansible-Inventory-Manager.git /tmp/xo-ansible-inventory-manager

# Create directories and copy files
sudo mkdir -p /usr/lib/xo-ansible-inventory-manager
sudo cp /tmp/xo-ansible-inventory-manager/src/lib/* /usr/lib/xo-ansible-inventory-manager/
sudo cp /tmp/xo-ansible-inventory-manager/example/xo_inventory.yaml /etc/ansible/

# Set permissions
sudo chmod +x /usr/lib/xo-ansible-inventory-manager/ansible-xo-inventory.py

# Create a symlink
sudo ln -s /usr/lib/xo-ansible-inventory-manager/ansible-xo-inventory.py /usr/bin/ansible-xo-inventory.py

echo "Installation complete."
```

## Removing the Plugin

### Removing the .deb Package

To remove the plugin installed via the `.deb` package, use the `dpkg -r` command.

```sh
sudo dpkg -r xo-ansible-inventory-manager
```

### Manual Removal Script

Here are the commands to manually remove this plugin.

```bash
#!/bin/bash
set -e

# Remove the symlink
sudo rm -f /usr/bin/ansible-xo-inventory.py

# Remove logs
sudo rm -f /var/log/ansible-inventory-loader.log

# Remove the plugin's configuration
sudo rm -f /etc/ansible/xo_inventory.yaml

# Nuke anything left in the lib folder
sudo rm -rf /usr/lib/xo-ansible-inventory-manager

echo "Removal complete."
```