"""
Testing iam builder inputs against expected outputs
"""

import unittest
import os
import yaml
import json

from parameterized import parameterized

from iam_builder.iam_builder import build_iam_policy

config_base_path = "tests/test_config"
test_policy_base_path = "tests/expected_policy"


def assert_config_as_expected(ut, config_name):
    with open(os.path.join(config_base_path, config_name + ".yaml")) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    with open(os.path.join(test_policy_base_path, config_name + ".json")) as f:
        expected = json.load(f)

    out = build_iam_policy(config)
    ut.assertDictEqual(out, expected)


def assert_config_error(ut, config_name):
    with open(os.path.join(config_base_path, config_name + ".yaml")) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    with ut.assertRaises(KeyError):
        build_iam_policy(config)


class TestExampleConfigs(unittest.TestCase):
    "Test examples in package"

    def test_examples(self):
        with open("examples/iam_config.yaml") as f:
            config_y = yaml.load(f, Loader=yaml.FullLoader)

        with open("examples/iam_config.json") as f:
            config_j = json.load(f)

        with open("examples/iam_policy.json") as f:
            expected = json.load(f)

        out_y = build_iam_policy(config_y)
        out_j = build_iam_policy(config_j)

        self.assertDictEqual(config_j, config_y)
        self.assertDictEqual(out_y, expected)
        self.assertDictEqual(out_j, expected)


class TestConfigOutputs(unittest.TestCase):
    """
    Test different configs
    """
    maxDiff = None
    
    @parameterized.expand(
        [
            "read_only",
            "write_only",
            "read_write",
            "sub_folder_multi_access",
            "athena_read_only",
            "athena_full_access",
            "glue_job",
            "all_config",
        ]
    )

    def test_config_output(self, config_name):
        assert_config_as_expected(self, config_name)


class TestBadConfigs(unittest.TestCase):
    """
    TEST Dodgy configs
    """

    @parameterized.expand(["bad_athena_config", "bad_glue_config"])
    def test_config_error(self, config_name):
        assert_config_error(self, config_name)
