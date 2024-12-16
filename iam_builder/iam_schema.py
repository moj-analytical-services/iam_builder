import jsonschema
import json
from iam_builder.exceptions import IAMValidationError

try:
    import pkg_resources
except Exception as e:
    print("Error importing pkg_resources", e)
    import importlib


try:
    IAM_SCHEMA = json.load(
        pkg_resources.resource_stream(__name__, "schemas/iam_schema.json")
    )
except ImportError:
    ref = importlib_resources.files(__name__).joinpath("schemas/iam_schema.json")
    with ref.open('rb') as fp:
        IAM_SCHEMA = json.load(
            fp.read()
        )


def validate_iam(config: dict):
    try:
        jsonschema.validate(instance=config, schema=IAM_SCHEMA)
    except jsonschema.ValidationError as e:
        raise IAMValidationError(f"Invalid IAM configuration, error:\n{e}")
