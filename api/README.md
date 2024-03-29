# Menu Sender API

## Development

If you have install more dependencies, you must add them to the `requirements.txt` file

```bash
python -m pip freeze > requirements.txt
```

To install requirements into your venv:

```bash
pip install -r requirements.txt
```

### Create your virtual environment in Python

```bash
python -m venv env
```

Enter your venv:

```bash
env/Scripts/activate
```

You must install the vscode extension PyLint to use the `.pylintrc` file for linting.

## DB Migration

1. Create the `migrations` folder (only done once!).

    ```bash
    flask db init
    ```

2. Generate a migration file

    ```bash
    flask db migrate -m "Initial migration."
    ```

3. Apply the migration:

    ```bash
    flask db upgrade
    ```
