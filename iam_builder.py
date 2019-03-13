import argparse
import json
import yaml

def main(config_path, out_path):
    with open('templates/iam_base_template.json') as f:
        iam = json.load(f)
    with open('templates/iam_lookup.json') as f:
        iam_lookup = json.load(f)

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

        if config['athena']['read_write_access']:
            iam['Statement'].extend(iam_lookup["athena_write_access"])

    # Test to run glue jobs
    if 'run_glue_job' in config:
        iam['Statement'].extend(iam_lookup['run_glue_job'])
        # Add ability to pass itself to glue job
        PassRoleToGlueService = {
            "Sid": "PassRoleToGlueService",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole"
            ],
            "Resource": "arn:aws:iam::593291632749:role/" + config['run_glue_job']['iam_role'],
            "Condition": {
                "StringLike": {
                    "iam:PassedToService": [
                        "glue.amazonaws.com"
                    ]
                }
            }
        }
        iam['Statement'].append(PassRoleToGlueService)

    # Deal with read only access
    list_buckets = []
    if 'read_only_s3_access' in config:
        s3_read_only = {
            "Sid": "readonly",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectAcl",
                "s3:GetObjectVersion",
            ],
            "Effect": "Allow",
            "Resource": config['read_only_s3_access'],
        }
        iam['Statement'].append(s3_read_only)

        # Get buckets to list
        list_buckets.extend(['arn:aws:s3:::' + p.split('/')[0] for p in config['read_only_s3_access']])

    # Deal with write only access
    if 'read_write_s3_access' in config:
        s3_read_write = {
            "Sid": "readwrite",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectAcl",
                "s3:GetObjectVersion",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion",
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:RestoreObject",
            ],
            "Effect": "Allow",
            "Resource": config['read_write_s3_access'],
        }
        iam['Statement'].append(s3_read_write)

        # Get buckets to list
        list_buckets.extend(['arn:aws:s3:::' + p.split('/')[0] for p in config['read_write_s3_access']])

    if list_buckets:
        s3_list_bucket = {
            "Sid": "list",
            "Action": [
                "s3:ListBucket"
            ],
            "Effect": "Allow",
            "Resource": list(set(list_buckets)),
        }
        iam['Statement'].append(s3_list_bucket)
    
    with open(out_path, "w+") as outfile:
        json.dump(iam, outfile, indent=4, separators=(',', ': '))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="path to your yaml/json config")
    parser.add_argument("-o", "--output", help="output_path")
    args = parser.parse_args()
    main(args.config, args.output)