import jsonschema
import json
import pkg_resources

IAM_SCHEMA = json.load(
    pkg_resources.resource_stream(__name__, "schemas/iam_schema.json")
)


def validate_iam(config: dict):
    jsonschema.validate(instance=config, schema=IAM_SCHEMA)
