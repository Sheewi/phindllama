from jsonschema import validate, ValidationError
import json

class DataValidator:
    def __init__(self):
        with open('schemas/data_lake.json') as f:
            self.schema = json.load(f)
    
    def validate_record(self, record_type: str, data: dict) -> bool:
        try:
            validate(instance=data, schema=self.schema[record_type])
            return True
        except ValidationError as e:
            print(f"Validation error: {e.message}")
            return False