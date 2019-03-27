"""
Testing IAM comfigurations work as expected
"""
import unittest

from etl_manager.etl import GlueJob
from gluejobutils import s3

from tests import (
    boto3,
    iam,
    init_role_and_add_single_policy_from_config
)

class TestS3Config(unittest.TestCase):
    """
    Test S3 configuration
    """
    def test_read_only(self):
        """
        Test read only access
        """
        c_path = 'tests/test_configs/readonly.yaml'
        init_role_and_add_single_policy_from_config('iam_builder_test_role', c_path)


        s3.read_json_from_s3('s3://alpha-test-iam-builer/read_only/test.json')
        s3.read_json_from_s3('s3://alpha-test-iam-builer/write_only/test.json')




    def test_write_only(self):
        """
        Test write only access
        """

    def test_read_write(self):
        """
        Test read_write_acess
        """

class TestAthenaConfig(unittest.TestCase):
    """
    Test to see if can run athena queries (Read/write)
    """
    def test_athena_read_only(self):

    def test_athena_write(self):

class TestGlueconfig(unittest.TestCase):
    """
    Test to see if can run a glue job with Glue test config
    """