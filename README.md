# IAM Builder

[![Publish](https://github.com/moj-analytical-services/iam_builder/actions/workflows/poetry-pypi-release.yml/badge.svg)](https://github.com/moj-analytical-services/iam_builder/actions/workflows/poetry-pypi-release.yml)

A python script to generate an IAM policy based on a yaml or json configuration.

To install:

```bash
# Most stable
pip install iam-builder

# OR directly from github
pip install git+git://github.com/moj-analytical-services/iam_builder.git#egg=iam_builder
```

To use the command line interface:

```bash
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

secretsmanager:
  read_only:
    - test_secret

s3:
  read_only:
    - test_bucket_read_only/*

  write_only:
    - test_bucket_write_only/*
    - test_bucket_read_only/write_only_folder/*

  read_write:
    - test_bucket_read_write/*
    - test_bucket_read_only/write_folder/*

  deny:
    - test_bucket_read_write/sensitive_table/*

kms:
  - test_kms_key_arn

bedrock: true
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
  },
  "kms": ["test_kms_key_arn"],
  "bedrock": true,
  "cloudwatch_athena_query_executions": true
}
```

- **iam_role_name:** The role name of your airflow job; required if you want to run glue jobs or access secrets.

- **athena:** Can have two keys.
  - **write**: Either `true` or `false`. If `false` then only read access to Athena (cannot create, delete or alter tables, databases and partitions). If `true` then the role will also have the ability to do stuff like CTAS queries, `DROP TABLE`, `CREATE DATABASE`, etc.
  - **dump_bucket**: The location in S3 (either an S3 path or a list of S3 paths) for temporarily storing the results of queries. This defaults to `mojap-athena-query-dump` and should not normally need changing.

- **is_cadet_deployer:** Boolean; Gives access to a highly empowered Glue role for Create-A-Derived-Table deployments. Will fail to apply if the `iam_role_name` doesn't include `cadet` in the string. Gives the user full control over all glue and athena structures in the named account.

- **glue_job:** Boolean; must be set to `true` to allow role to run glue jobs. If `false` or absent role will not be able to run glue jobs.

- **secrets:** Boolean or string; must be set to `true` or `"read"` to allow role to access secrets from AWS Parameter Store, and `readwrite` to provide read/write access. If `false` or absent role will not be able to access secrets.

- **s3:** Can have up to 4 keys: `read_only`, `write_only`, `read_write`, and `deny`. Each key describes the level of access you want your iam policy to have with each s3 path. More details below:

  - **read_only:** A list of s3 paths that the iam_role should be able to access (read only). Each item in the list should either be a path to a object or finish with `/*` to denote that it can access everything within that directory. _Note the S3 paths don't start with `s3://` in the config._

  - **write_only:** A list of s3 paths that the iam_role should be able to access (write only). Each item in the list should either be a path to a object or finish with `/*` to denote that it can access everything within that directory. _Note the S3 paths don't start with `s3://` in the config._

  - **read_write:** A list of s3 paths that the iam_role should be able to access (read and write). Each item in the list should either be a path to a object or finish with `/*` to denote that it can access everything within that directory. _Note the S3 paths don't start with `s3://` in the config._

  - **deny:** A list of s3 paths that the iam_role should _not_ be able to access. This should be used to add exceptions to wildcarded access to folders, for example excluding sensitive tables in order to provide basic access to a database. Each item in the list should either be a path to a object or finish with `/*` to denote that it can access everything within that directory. _Note the S3 paths don't start with `s3://` in the config._

- **kms:** A list of kms arns that the iam_role should be able to access. Can call the DescribeKey, GenerateDataKey, Decrypt, Encrypt and ReEncrypt
  operations.

- **secretsmanager:** A secret that the iam_role should be able to access. Can call the GetSecretValue, DescribeSecret and ListSecrets operations.

- **bedrock:** Boolean; must be set to `true` to allow role to interact with Amazon Bedrock. If `false` or absent role will not be able to interact with Amazon Bedrock.

- **cloudwatch_athena_query_executions** Boolean; must be set to `true` to allow role to read `cloudtrail-athena-events` log group. If `false` or absent role will not be able to read these cloudwatch logs.

## How to update

When updating IAM builder, make sure to change the version number in `pyproject.toml` and describe the change in `CHANGELOG.md`.

If you have changed any dependencies in `pyproject.yaml`, run `poetry update` to update `poetry.lock`.

Once you have created a release in GitHub, a Github Action will run to publish the release on PyPI automatically.

