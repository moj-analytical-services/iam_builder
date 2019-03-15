# IAM Builder

In development as no UTs yet.

A python script to generate an IAM policy based on an yaml (done) or json config. Not very well structured atm but does the job. Also not unit tested...

To install (currently a private repo):

```
pip install git+ssh://git@github.com/moj-analytical-services/iam_builder.git@#egg=iam_builder
```

In python:

```python
from iam_builder.iam_builder import build_iam_policy

build_iam_policy("examples/iam_config.yaml', 'examples/iam_policy.json')
```

or in bash:

```
iam_builder -c examples/iam_config.yaml -o examples/iam_policy.json
```

Will output the iam_policy seen in the examples folder.

Your config file can be either a yaml file or json.

The example yaml (`iam_config.yaml`) looks this:

```yaml
athena:
  read_write_access: false

run_glue_job:
  iam_role: iam_role_name

read_only_s3_access:
  - test_bucket_read_only/*

read_write_s3_access:
  - test_bucket_read_write/*
  - test_bucket_read_only/write_folder/*
```

Whilst the example json (`iam_config.json`) looks like this:

```json
{
    "athena": {
        "read_write_access": false
    },
    "run_glue_job": {
        "iam_role": "iam_role_name"
    },
    "read_only_s3_access": [
        "test_bucket_read_only/*"
    ],
    "read_write_s3_access": [
        "test_bucket_read_write/*",
        "test_bucket_read_only/write_folder/*"
    ]
}
```

- **athena:** only has one key value pair. `read_write_access` which is either true or false. If `false` then only read access to athena. If `true` then the role will also have the ability to do stuff like CTAS queries, `DROP TABLE`, `CREATE DATABASE`, etc.

- **run_glue_job:** Allows role to run glue jobs. Requires an iam_role parameter which should be the name of the iam role that you are creating.

- **read_only_s3_access:** A list of s3 paths that the iam_role should be able to access (read only). Each item in the list should either be a path to a object or finish with `/*` to denote that it can access everything within that directory. _Note the S3 paths don't start with `s3://` in the config._

- **write_only_s3_access:** A list of s3 paths that the iam_role should be able to access (read and write). Each item in the list should either be a path to a object or finish with `/*` to denote that it can access everything within that directory. _Note the S3 paths don't start with `s3://` in the config._