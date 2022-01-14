import jsonschema
import json
import pkg_resources
from iam_builder.exceptions import IAMValidationError

IAM_SCHEMA = json.load(
    pkg_resources.resource_stream(__name__, "schemas/iam_schema.json")
)


def validate_iam(config: dict):
    try:
        jsonschema.validate(instance=config, schema=IAM_SCHEMA)
    except jsonschema.ValidationError as e:
        raise IAMValidationError(f"Invalid IAM configuration, error:\n{e}")
