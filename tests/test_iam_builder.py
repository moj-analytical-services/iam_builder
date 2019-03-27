
# -*- coding: utf-8 -*-

"""
Testing DatabaseMeta, TableMeta
"""

import unittest
import os
import yaml
import json

from iam_builder.iam_builder import build_iam_policy

config_base_path = 'tests/test_config'
test_policy_base_path = 'tests/expected_policy'

class TestConfigOutputs(unittest.TestCase):
    """
    Test different configs
    """
    def test_read_only(self):
        config_name = 'read_only'
        with open(os.path.join(config_base_path, config_name + '.yaml')) as f:
            config = yaml.load(f)
        with open(os.path.join(test_policy_base_path, config_name + '.json')) as f:
            expected = json.load(f)
           
        out = build_iam_policy(config)
        self.assertDictEqual(out, expected)
    
    def test_write_only(self):
        config_name = 'write_only'
        with open(os.path.join(config_base_path, config_name + '.yaml')) as f:
            config = yaml.load(f)
        with open(os.path.join(test_policy_base_path, config_name + '.json')) as f:
            expected = json.load(f)
           
        out = build_iam_policy(config)
        self.assertDictEqual(out, expected)
    
    def test_read_write(self):
        config_name = 'read_write'
        with open(os.path.join(config_base_path, config_name + '.yaml')) as f:
            config = yaml.load(f)
        with open(os.path.join(test_policy_base_path, config_name + '.json')) as f:
            expected = json.load(f)
           
        out = build_iam_policy(config)
        self.assertDictEqual(out, expected)
    
    def test_sub_folder_multi_access(self):
        config_name = 'sub_folder_multi_access'
        with open(os.path.join(config_base_path, config_name + '.yaml')) as f:
            config = yaml.load(f)
        with open(os.path.join(test_policy_base_path, config_name + '.json')) as f:
            expected = json.load(f)
           
        out = build_iam_policy(config)
        self.assertDictEqual(out, expected)
    
    def test_athena_read_only(self):
        config_name = 'athena_read_only'
        with open(os.path.join(config_base_path, config_name + '.yaml')) as f:
            config = yaml.load(f)
        with open(os.path.join(test_policy_base_path, config_name + '.json')) as f:
            expected = json.load(f)
           
        out = build_iam_policy(config)
        self.assertDictEqual(out, expected)

    def test_athena_full_access(self):
        config_name = 'athena_full_access'
        with open(os.path.join(config_base_path, config_name + '.yaml')) as f:
            config = yaml.load(f)
        with open(os.path.join(test_policy_base_path, config_name + '.json')) as f:
            expected = json.load(f)
           
        out = build_iam_policy(config)
        self.assertDictEqual(out, expected)

    def test_glue_job(self):
        config_name = 'glue_job'
        with open(os.path.join(config_base_path, config_name + '.yaml')) as f:
            config = yaml.load(f)
        with open(os.path.join(test_policy_base_path, config_name + '.json')) as f:
            expected = json.load(f)
           
        out = build_iam_policy(config)
        self.assertDictEqual(out, expected)

    def test_all_config(self):
        config_name = 'all_config'
        with open(os.path.join(config_base_path, config_name + '.yaml')) as f:
            config = yaml.load(f)
        with open(os.path.join(test_policy_base_path, config_name + '.json')) as f:
            expected = json.load(f)
           
        out = build_iam_policy(config)
        self.assertDictEqual(out, expected)

class TestBadConfigs(unittest.TestCase):
    """
    TEST Dodgy configs
    """
    def test_bad_athena_config(self):
        config_name = 'bad_athena_config'
        with open(os.path.join(config_base_path, config_name + '.yaml')) as f:
            config = yaml.load(f)

        with self.assertRaises(KeyError):
            out = build_iam_policy(config)
    
    def test_bad_glue_config(self):
        config_name = 'bad_glue_config'
        with open(os.path.join(config_base_path, config_name + '.yaml')) as f:
            config = yaml.load(f)

        with self.assertRaises(KeyError):
            out = build_iam_policy(config)
    