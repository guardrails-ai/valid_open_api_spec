# to run these, run 
# pytest test/test-validator.py

import json
from guardrails import Guard
import pytest
from validator import ValidOpenApiSpec

from .specs import valid, invalid

# We use 'refrain' as the validator's fail action,
#  so we expect failures to always result in a guarded output of None
# Learn more about corrective actions here:
#  https://www.guardrailsai.com/docs/concepts/output/#%EF%B8%8F-specifying-corrective-actions
guard = Guard.from_string(validators=[ValidOpenApiSpec(on_fail="exception")])

def test_pass():
    result = guard.parse(json.dumps(valid))
    assert result.validation_passed is True
    assert result.validated_output == json.dumps(valid)

def test_fail():
    with pytest.raises(Exception) as excinfo:
        guard.parse(json.dumps(invalid))

    assert str(excinfo.value).strip() == """Validation failed for field with errors: Value is not a valid OpenAPI Specification.
The following fields are invalid:
{
  "$.info": [
    "'version' is a required property"
  ]
}"""
    
