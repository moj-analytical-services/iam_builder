# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## v4.10.0

- Add read Cloudtrail event permission

## v4.9.0

- Add `external_iam_role` to allow Airflow Pulumi tests to pass

## v4.8.0

- Updates standard athena policy to add 'glue:GetTableVersions'

## v4.7.0

- Add London region for Amazon Bedrock

## v4.6.0

- Add Amazon Bedrock permissions

## v4.5.0

- added Get/Put Object Tagging permissions for S3 readwrite access

## v4.4.0

- added GetTableMetadata to Athena read policy

## v4.3.0

- added kms permissions

## v4.2.2

- updated pypi action for trusted publisher

## v4.2.1

- implemented backwards compatibility for secrets

## v4.2.0

- added readwrite option for secrets
- add deny option to s3 access

## v4.1.2

- Updated dependencies.

## v4.1.1

- Loosened jsonschema version requirements.

## v4.1.0

- Added schema validation
- Removed support for Python 3.6

## v4.0.0

- Added details on how to update on PyPi
- Added Github action for linting
- Target bucket for Athena query temporary files can now be selected in config (or left out to use default)
- Changed default query dump bucket from alpha-athena-query-dump to mojap-athena-query-dump
- Can select multiple query dump buckets by putting a list in config
- Added a test for multiple query dump buckets
- Added some type hints

## v3.7.0

- Updated `parameterized` module dependency to align with `etl_manager`

## v3.6.0

- Updated Athena read and write policy templates to remove permissions to `ListBucket` on `aws-athena-query-results-*` and improve consistency

## v3.5.0

- Added additional permissions to glue jobs to write logs and metrics correctly
- Updated project toml

## v3.4.0
- Depreciated as project toml was not updated

## v3.3.0

- Reverting version back to v3.1.0 and releasing as a new version

## v3.2.0

- Seperated out list bucket policy into two seperate Sids for clarity
- Started using `pyproject.toml`

## v3.1.0

- Updated UTs and CI to GitHub Actions
- Started using `pyproject.toml`

## v3.0.0

- Added secrets parameters and access for users

## v2.0.0

### Changed

- Updated yaml read based on [this](https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation)
- Added `alpha-athena-dump` bucket to list bucket iam actions - required to work with `s3tools` package

## v1.2.3

### Changed

- removed f-strings and changed python requirements to 3.5 and above

## v1.2.0

### Added

- s3 action `GetBucketLocation` added to the `list` Sid in the IAM templates.

## v1.1.0

### Added

- s3 action `ListAllMyBuckets` added to the `list` Sid in the IAM templates.

## v1.0.0

Inital release
