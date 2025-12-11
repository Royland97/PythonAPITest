from bson import ObjectId
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from typing import Any

#Handler ObjectId with Pydantic
class PyObjectId(ObjectId):

    @classmethod
    def __get_pydantic_core_schema__(cls, _source, handler):
        return handler(
            "str"
        )

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: Any, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema
