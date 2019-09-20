# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

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