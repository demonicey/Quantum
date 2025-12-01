# Python Virtual Environment Setup and Package Management

This project uses a Python virtual environment to manage dependencies and isolate project-specific packages.

## Creating the Virtual Environment

The virtual environment has been created in the `.venv` directory using the following command:

```bash
python3 -m venv .venv
```

## Activating the Virtual Environment

To activate the virtual environment on macOS or Unix systems, use the following command:

```bash
source .venv/bin/activate
```

You will see your shell prompt change to indicate the environment is active, e.g.:

```
(.venv) $
```

## Managing Packages with pip

Once activated, you can install, upgrade, and uninstall packages using `pip`.

### Installing the latest version of a package

```bash
pip install package_name
```

### Installing a specific version of a package

```bash
pip install package_name==version_number
```

### Upgrading an installed package

```bash
pip install --upgrade package_name
```

### Uninstalling a package

```bash
pip uninstall package_name
```

### Listing installed packages

```bash
pip list
```

### Generating a `requirements.txt` file

```bash
pip freeze > requirements.txt
```

This file can be used to recreate the environment:

```bash
pip install -r requirements.txt
```

## Deactivating the Virtual Environment

To exit the virtual environment, simply run:

```bash
deactivate
