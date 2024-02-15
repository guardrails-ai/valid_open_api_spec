## Overview

| Developed by | Guardrails AI |
| --- | --- |
| Date of development | Feb 15, 2024 |
| Validator type | Format |
| Blog |  |
| License | Apache 2 |
| Input/Output | Output |

## Description

This validator ensures that a generated output is a valid OpenAPI Specification.

## Requirements
- Dependencies: `jsonschema`, `pytest`, `pyyaml`, `referencing`

## Installation

```bash
$ guardrails hub install hub://guardrails/valid_open_api_spec
```

## Usage Examples

### Validating string output via Python

In this example, we’ll test that a generated value is a valid OpenAPI spec.

```python
import json
# Import Guard and Validator
from guardrails.hub import ValidOpenApiSpec
from guardrails import Guard

# Initialize Validator
val = ValidOpenApiSpec()

# Setup Guard
guard = Guard.from_string(
    validators=[val, ...],
)

guard.parse(json.dumps({
    "openapi": "3.0.0",
    "info": {
        "title": "API",
        "version": "1.0.0"
    }
}))  # Validator passes
guard.parse(json.dumps({
    "openapi": "3.0.0",
    "info": {
        "title": "API"
    }
}))  # Validator fails; note the missing version
```

### Validating JSON output via Python

In this example, we verify that a user’s email is specified in lower case.

```python
# Import Guard and Validator
from pydantic import BaseModel
from guardrails.hub import LowerCase
from guardrails import Guard

val = ValidOpenApiSpec()

# Create Pydantic BaseModel
class ApiRecord(BaseModel):
    name: str
    endpoint: float
    api_spec: Dict = Field(validators=[ValidOpenApiSpec()])

# Create a Guard to check for valid Pydantic output
guard = Guard.from_pydantic(output_class=UserInfo)

# Run LLM output generating JSON through guard
guard.parse("""
{
        "name": "API",
        "endpoint": http://localhost:8000,
        "api_spec": {
            "openapi": "3.0.0",
            "info": {
                "title": "API",
                "version": "1.0.0"
            }
        }
}
""")
```

## API Reference

**`__init__(self, on_fail="noop")`**
<ul>

Initializes a new instance of the Validator class.

**Parameters:**

- **`on_fail`** *(str, Callable):* The policy to enact when a validator fails. If `str`, must be one of `reask`, `fix`, `filter`, `refrain`, `noop`, `exception` or `fix_reask`. Otherwise, must be a function that is called when the validator fails.

</ul>

<br>

**`__call__(self, value, metadata={}) → ValidationOutcome`**

<ul>

Validates the given `value` using the rules defined in this validator, relying on the `metadata` provided to customize the validation process. This method is automatically invoked by `guard.parse(...)`, ensuring the validation logic is applied to the input data.

Note:

1. This method should not be called directly by the user. Instead, invoke `guard.parse(...)` where this method will be called internally for each associated Validator.
2. When invoking `guard.parse(...)`, ensure to pass the appropriate `metadata` dictionary that includes keys and values required by this validator. If `guard` is associated with multiple validators, combine all necessary metadata into a single dictionary.

**Parameters:**

- **`value`** *(Any):* The input value to validate.
- **`metadata`** *(dict):* A dictionary containing metadata required for validation. No additional metadata keys are needed for this validator.

</ul>