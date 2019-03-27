"""
Testing IAM comfigurations work as expected
"""

import unittest
from etl_manager.etl import GlueJob
from gluejobutils import s3

from tests import iam, role_name, wait_for_policy_role_change,

class TestS3Config(unittest.TestCase):
    """
    Test 
    """
    def test_read_only(self):
        """
        Test read only access
        """




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