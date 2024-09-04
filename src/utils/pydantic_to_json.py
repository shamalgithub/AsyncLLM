import json
from typing import Dict, Any


"""   
pydantic_schema = MathResponse.model_json_schema()
transformed_schema = transform_schema(pydantic_schema)
print(json.dumps(transformed_schema, indent=2))
"""

def camel_to_snake(name: str) -> str:
    return ''.join(['_' + char.lower() if char.isupper() else char for char in name]).lstrip('_')

def transform_schema(pydantic_model: Any) -> Dict[str, Any]:
    schema = pydantic_model.model_json_schema()

    def process_property(prop: Dict[Any, Any]) -> Dict[Any, Any]:
        if "$ref" in prop:
            ref = prop["$ref"].split("/")[-1]
            return process_property(schema["$defs"][ref])
        
        if prop.get("type") == "array" and "items" in prop:
            prop["items"] = process_property(prop["items"])
        
        if prop.get("type") == "object":
            if "properties" in prop:
                for key, value in prop["properties"].items():
                    prop["properties"][key] = process_property(value)
            prop["additionalProperties"] = False
        
        return prop

    transformed_schema = {
        "type": "object",
        "properties": {},
        "required": schema.get("required", []),
        "additionalProperties": False
    }

    for key, value in schema["properties"].items():
        transformed_schema["properties"][key] = process_property(value)

    # Extract the title from the original schema and convert to snake_case
    schema_name = camel_to_snake(schema.get("title", pydantic_model.__name__))

    # Construct the final output
    result = {
        "type": "json_schema",
        "json_schema": {
            "name": schema_name,
            "strict": True,
            "schema": transformed_schema
        }
    }

    return result


