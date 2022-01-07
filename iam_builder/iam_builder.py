import copy
from typing import Union, List

from iam_builder.templates import (
    iam_base_template,
    iam_lookup,
    get_athena_read_access,
    get_pass_role_to_glue_policy,
    get_read_only_policy,
    get_write_only_policy,
    get_read_write_policy,
    get_s3_list_bucket_policy,
    get_secrets,
)


def check_is_list(
    config_path: List[str], list_to_check: Union[list, str]
) -> None:
    """
    Checks that an expected list is a list and raises a TypeError otherwise.
    """
    if not isinstance(list_to_check, list):
        m = "Expected a list but received a string. Try using\n"
        indent = ""
        for x in config_path:
            m += indent + x + ":\n"
            indent += "  "
        m += f"{indent}- {list_to_check}\n"
        raise TypeError(m)


def build_iam_policy(config: dict) -> dict:
    """
    Takes a configuration for an IAM policy and returns the policy as a dict.
    """
    iam: dict = copy.deepcopy(iam_base_template)

    list_buckets = []

    # Define if has athena permission
    if "athena" in config:
        dump_bucket = config["athena"].get(
            "dump_bucket", ["mojap-athena-query-dump"]
        )
        if not isinstance(dump_bucket, list):
            dump_bucket = [dump_bucket]
        dump_bucket = [bucket.replace("_", "-") for bucket in dump_bucket]

        iam["Statement"].extend(get_athena_read_access(dump_bucket))

        if config["athena"]["write"]:
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
            check_is_list(["s3", "read_only"], config["s3"]["read_only"])
            s3_read_only = get_read_only_policy(config["s3"]["read_only"])
            iam["Statement"].append(s3_read_only)

            # Get buckets to list
            list_buckets.extend(
                [p.split("/")[0] for p in config["s3"]["read_only"]]
            )

        if "write_only" in config["s3"]:
            check_is_list(["s3", "write_only"], config["s3"]["write_only"])
            s3_write_only = get_write_only_policy(config["s3"]["write_only"])
            iam["Statement"].append(s3_write_only)

            # Get buckets to list
            list_buckets.extend(
                [p.split("/")[0] for p in config["s3"]["write_only"]]
            )

        # Deal with write only access
        if "read_write" in config["s3"]:
            check_is_list(["s3", "read_write"], config["s3"]["read_write"])
            s3_read_write = get_read_write_policy(config["s3"]["read_write"])
            iam["Statement"].append(s3_read_write)

            # Get buckets to list
            list_buckets.extend(
                [p.split("/")[0] for p in config["s3"]["read_write"]]
            )

    if list_buckets:
        s3_list_bucket = get_s3_list_bucket_policy(list_buckets)
        iam["Statement"].append(s3_list_bucket)

    if "secrets" in config and config["secrets"]:
        secrets_statement = get_secrets(config["iam_role_name"])
        iam["Statement"].append(secrets_statement)
        iam["Statement"].extend(iam_lookup["decrypt_statement"])

    return iam
