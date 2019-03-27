import boto3
from time import sleep

iam = boto3.client('iam')

role_name = 'iam_builder_test_role'

def remove_all_roles_from_policy(role_name):
    list_of_policies = iam.list_role_policies(RoleName=role_name)
    for p in list_of_policies:
        response = iam.delete_role_policy(
            RoleName=role_name,
            PolicyName='read_only'
        )

def wait_for_policy_role_change(role_name, policy_name = None, num_checks = 5, wait_time = 2):
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
