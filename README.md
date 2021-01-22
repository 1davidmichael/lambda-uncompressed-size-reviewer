# Total Lambda Size

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python total_lambda_size.py itdev-rate-repository-q-subscriber

/tmp/tmp57a59twu/itdev-rate-repository-q-subscriber.zip: 103M
/tmp/tmp57a59twu/postgres-driver-layer.zip: 7M
/tmp/tmp57a59twu/pyodbc-driver-layer.zip: 13M
/tmp/tmp57a59twu/snowflake-lite-driver-layer-test.zip: 105M
Total: 230M
```