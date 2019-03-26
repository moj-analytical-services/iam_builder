import json
import yaml

from iam_builder.templates import (
    iam_base_template as iam,
    iam_lookup,
    get_pass_role_to_glue_policy,
    get_read_only_policy,
    get_write_only_policy,
    get_read_write_policy,
    get_s3_list_bucket_policy
)

def build_iam_policy(config_path, out_path):
    # Assume config is a yaml file if not json
    if config_path.endswith('.json'):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        with open(config_path, 'r') as f:
            config = yaml.load(f)

    # Define if has athena permission
    if 'athena' in config:
        iam['Statement'].extend(iam_lookup["athena_read_access"])

        if config['athena']['write']:
            iam['Statement'].extend(iam_lookup["athena_write_access"])

    # Test to run glue jobs
    if 'glue_job' in config:
        iam['Statement'].extend(iam_lookup['glue_job'])
        # Add ability to pass itself to glue job
        pass_role = get_pass_role_to_glue_policy(config['glue_job']['iam_role_name'])
        iam['Statement'].append(pass_role)

    # Deal with read only access
    list_buckets = []
    if 's3' in config:
        if 'read_only' in config['s3']:
            s3_read_only = get_read_only_policy(config['s3']['read_only'])
            iam['Statement'].append(s3_read_only)

            # Get buckets to list
            list_buckets.extend([p.split('/')[0] for p in config['s3']['read_only']])

        if 'write_only' in config['s3']:
            s3_write_only = get_write_only_policy(config['s3']['write_only'])
            iam['Statement'].append(s3_write_only)

            # Get buckets to list
            list_buckets.extend([p.split('/')[0] for p in config['s3']['write_only']])

        # Deal with write only access
        if 'read_write' in config['s3']:
            s3_read_write = get_read_write_policy(config['s3']['read_write'])
            iam['Statement'].append(s3_read_write)

            # Get buckets to list
            list_buckets.extend([p.split('/')[0] for p in config['s3']['read_write']])

    if list_buckets:
        s3_list_bucket = get_s3_list_bucket_policy(list_buckets)
        iam['Statement'].append(s3_list_bucket)

    with open(out_path, "w+") as outfile:
        json.dump(iam, outfile, indent=4, separators=(',', ': '))
