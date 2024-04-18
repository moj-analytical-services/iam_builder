import copy

from iam_builder.templates import (
    iam_base_template,
    iam_lookup,
    get_athena_read_access,
    get_pass_role_to_glue_policy,
    get_read_only_policy,
    get_write_only_policy,
    get_read_write_policy,
    get_deny_policy,
    get_s3_list_bucket_policy,
    get_secrets,
    get_kms_permissions
)
from iam_builder.iam_schema import validate_iam


def build_iam_policy(config: dict) -> dict:  # noqa: C901
    """
    Takes a configuration for an IAM policy and returns the policy as a dict.
    """
    validate_iam(config)

    iam: dict = copy.deepcopy(iam_base_template)

    list_buckets = []

    # Define if has athena permission
    if "athena" in config:
        dump_bucket = config["athena"].get("dump_bucket", ["mojap-athena-query-dump"])
        if not isinstance(dump_bucket, list):
            dump_bucket = [dump_bucket]
        dump_bucket = [bucket.replace("_", "-") for bucket in dump_bucket]

        iam["Statement"].extend(get_athena_read_access(dump_bucket))

        if config["athena"].get("write", False):
            iam["Statement"].extend(iam_lookup["athena_write_access"])

        # Needed for s3tools package
        list_buckets.extend(dump_bucket)

    # Test to run glue jobs
    if "glue_job" in config and config["glue_job"]:
        iam["Statement"].extend(iam_lookup["glue_job"])
        # Add ability to pass itself to glue job
        pass_role = get_pass_role_to_glue_policy(config["iam_role_name"])
        iam["Statement"].append(pass_role)

    # Deal with read only access
    if "s3" in config:
        if "read_only" in config["s3"]:
            s3_read_only = get_read_only_policy(config["s3"]["read_only"])
            iam["Statement"].append(s3_read_only)

            # Get buckets to list
            list_buckets.extend([p.split("/")[0] for p in config["s3"]["read_only"]])

        # Deal with write only access
        if "write_only" in config["s3"]:
            s3_write_only = get_write_only_policy(config["s3"]["write_only"])
            iam["Statement"].append(s3_write_only)

            # Get buckets to list
            list_buckets.extend([p.split("/")[0] for p in config["s3"]["write_only"]])

        if "read_write" in config["s3"]:
            s3_read_write = get_read_write_policy(config["s3"]["read_write"])
            iam["Statement"].append(s3_read_write)

            # Get buckets to list
            list_buckets.extend([p.split("/")[0] for p in config["s3"]["read_write"]])

        if "deny" in config["s3"]:
            s3_deny = get_deny_policy(config["s3"]["deny"])
            iam["Statement"].append(s3_deny)

            # Get buckets to list
            list_buckets.extend([p.split("/")[0] for p in config["s3"]["deny"]])

    if list_buckets:
        s3_list_bucket = get_s3_list_bucket_policy(list_buckets)
        iam["Statement"].append(s3_list_bucket)

    if "secrets" in config:
        secrets = config["secrets"]
        if isinstance(secrets, str) or secrets:
            readwrite = secrets == "readwrite"
            secrets_statement = get_secrets(config["iam_role_name"], readwrite)
            iam["Statement"].append(secrets_statement)
            iam["Statement"].extend(iam_lookup["decrypt_statement"])

    if "kms" in config:
        kms_arns = config["kms"]
        kms_permissions = get_kms_permissions(kms_arns)
        iam["Statement"].append(kms_permissions)

    return iam
