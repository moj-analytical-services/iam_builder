import jsonschema
import json
from iam_builder.exceptions import IAMValidationError
import importlib_resources


ref = importlib_resources.files(__name__).joinpath("schemas/iam_schema.json")
with ref.open('rb') as fp:
    IAM_SCHEMA = json.load(
        fp
    )


def validate_iam(config: dict):
    try:
        jsonschema.validate(instance=config, schema=IAM_SCHEMA)
    except jsonschema.ValidationError as e:
        raise IAMValidationError(f"Invalid IAM configuration, error:\n{e}")
