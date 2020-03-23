# IAM Builder

[![Actions Status](https://github.com/moj-analytical-services/iam_builder/workflows/IAM%20Builder/badge.svg)](https://github.com/moj-analytical-services/iam_builder/actions)

A python script to generate an IAM policy based on an yaml or json configuration.

To install:

```
# Most stable
pip install iam-builder

# OR directly from github
pip install git+git://github.com/moj-analytical-services/iam_builder.git#egg=iam_builder
```

To use the command line interface:

```
iam_builder -c examples/iam_config.yaml -o examples/iam_policy.json
```

- `-c` is the path to your iam configuration (either a yaml or json file).
- `-o` is the path to your output iam policy (needs to be a json file).

Or to do the same thing in python:

```python
import yaml
import json
from iam_builder.iam_builder import build_iam_policy

with open('examples/iam_config.yaml') as f:
  config = yaml.load(f, Loader=yaml.FullLoader)

iam_policy = build_iam_policy(config)

with open('examples/iam_policy.json', "w+") as f:
  json.dump(iam_policy, f, indent=4, separators=(',', ': '))
```

Both scripts will create the output iam_policy seen in the [examples](examples/) folder. You can also see [more example configs](tests/test_config/) by looking in the unit tests.

Your config file can be either a yaml or json file.

The example yaml (`iam_config.yaml`) looks this:

```yaml
iam_role_name: iam_role_name

athena:
  write: false

glue_job: true

secrets: true

s3: 
  read_only:
    - test_bucket_read_only/*

  write_only:
    - test_bucket_write_only/*
    - test_bucket_read_only/write_only_folder/*

  read_write:
    - test_bucket_read_write/*
    - test_bucket_read_only/write_folder/*
```

Whilst the example json (`iam_config.json`) looks like this:

```json
{
  "iam_role_name": "iam_role_name",
  "athena": {
    "write": false
  },
  "glue_job": true,
  "secrets": true,
  "s3": {
    "read_only": [
      "test_bucket_read_only/*"
    ],
    "write_only": [
      "test_bucket_write_only/*",
      "test_bucket_read_only/write_only_folder/*"
    ],
    "read_write": [
      "test_bucket_read_write/*",
      "test_bucket_read_only/write_folder/*"
    ]
  }
}
```
- **iam_role_name:** The role name of your airflow job; required if you want to run glue jobs or access secrets.

- **athena:** Only has one key value pair. `write` which is either true or false. If `false` then only read access to Athena (cannot create, delete or alter tables, databases and partitions). If `true` then the role will also have the ability to do stuff like CTAS queries, `DROP TABLE`, `CREATE DATABASE`, etc.

- **glue_job:** Boolean; must be set to `true` to allow role to run glue jobs. If `false` or absent role will not be able to run glue jobs.

- **secrets:** Boolean; must be set to `true` to allow role to access secrets from AWS Parameter Store. If `false` or absent role will not be able to access secrets.

- **s3:** Can have up to 3 keys: `read_only`, `write_only` and `read_write`. Each key describes the level of access you want your iam policy to have with each s3 path. More details below:
  
  - **read_only:** A list of s3 paths that the iam_role should be able to access (read only). Each item in the list should either be a path to a object or finish with `/*` to denote that it can access everything within that directory. _Note the S3 paths don't start with `s3://` in the config._

  - **write_only:** A list of s3 paths that the iam_role should be able to access (write only). Each item in the list should either be a path to a object or finish with `/*` to denote that it can access everything within that directory. _Note the S3 paths don't start with `s3://` in the config._

  - **read_write_s3_access:** A list of s3 paths that the iam_role should be able to access (read and write). Each item in the list should either be a path to a object or finish with `/*` to denote that it can access everything within that directory. _Note the S3 paths don't start with `s3://` in the config._

## How to update

When updating IAM builder, make sure to change the version number in `pyproject.yaml` and describe the change in `CHANGELOG.md`.

If you have changed any dependencies in `pyproject.yaml`, run `poetry update` to update `poetry.lock`.

Once you have created a release in GitHub, to publish the latest version to PyPI, run:

```
poetry build
poetry publish -u <username>
```

Here, you should substitute `<username>` for your PyPI username. In order to publish to PyPI, you must be an owner of the project.
