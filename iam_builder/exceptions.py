from jsonschema import ValidationError


class IAMValidationError(ValidationError):
    pass


class PrivilegedRoleValidationError(ValueError):
    pass
