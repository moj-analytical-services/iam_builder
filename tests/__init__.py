import json
import yaml

import boto3
from time import sleep

from iam_builder.iam_builder import build_iam_policy


iam = boto3.client('iam')

def remove_all_polices_from_role(role_name):
    list_of_policies = iam.list_role_policies(RoleName=role_name)
    for p in list_of_policies:
        response = iam.delete_role_policy(
            RoleName=role_name,
            PolicyName=p
        )

def wait_for_policy_role_change(role_name, policy_name=None, num_checks=5, wait_time=2):
    """
    Wait for a policy to either have no policies or have a policy added.
    If policy_name is None then excepts no policies to be added to role.
    """

    i = 0
    if policy_name:
        test_fun = lambda p, l: p in l
    else:
        test_fun = lambda p, l: len(l) == 0

    # Do check
    while i < num_checks:
        response = iam.list_role_policies(RoleName=role_name)
        if test_fun(policy_name, response['PolicyNames']):
            break
        else:
            i += 1
            sleep(wait_time)

    # Check that changes took affect
    if i >= num_checks:
        list_policy_names = ', '.join(response['PolicyNames'])
        raise TimeoutError(f"Timed Out: Policy change did not take affect. PolicyNames: {list_policy_names}. Try upping the number of wait_time or num_check args.")

def init_role_and_add_single_policy_from_config(role_name, config_path):
    remove_all_polices_from_role(test_role_name)
    wait_for_policy_role_change(role_name, policy_name=None)

    with open(config_path, 'r') as f:
        policy_config = yaml.load(f)

    policy_doc = build_iam_policy(policy_config)
    iam.put_role_policy(
        RoleName=test_role_name,
        PolicyName='test_policy',
        PolicyDocument=json.dumps(policy_doc)
    )

    wait_for_policy_role_change(role_name, policy_name='test_policy')