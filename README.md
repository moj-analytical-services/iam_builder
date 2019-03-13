# IAM Builder

In development.

A python script to generate an IAM policy based on an yaml (done) or json config (not yet done). Not very well structured atm but does the job. Also not unit tested...

In python:

```python
from iam_builder import main as build_iam

build_iam("examples/testing.yaml', 'examples/iam_policy.json')
```

or in bash:

```
python iam_builder.py -c examples/testing.yaml -o examples/iam_policy.json
```

Will output the iam_policy seen in the examples folder.

Your config file can be either a yaml file or json.

The example yaml looks this:

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

Whilst the example json looks like this:

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