#!/bin/bash

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Confirm python version and environment
echo "Python version:"
python --version

echo "PIP version:"
pip --version

# Install a specific version of a package (requests 2.25.1)
echo "Installing requests==2.25.1..."
pip install requests==2.25.1

# List installed packages
echo "Listing installed packages after install:"
pip list

# Show information about requests package
echo "Showing info about requests package:"
pip show requests

# Upgrade requests package to latest version
echo "Upgrading requests package to the latest version..."
pip install --upgrade requests

# List installed packages after upgrade
echo "Listing installed packages after upgrade:"
pip list

# Freeze installed packages to requirements.txt
echo "Freezing installed packages to requirements.txt..."
pip freeze > requirements.txt
cat requirements.txt

# Uninstall requests package
echo "Uninstalling requests package..."
pip uninstall -y requests

# Confirm uninstall by listing packages
echo "Listing installed packages after uninstall:"
pip list

# Deactivate virtual environment
echo "Deactivating virtual environment..."
deactivate

echo "Testing completed."
