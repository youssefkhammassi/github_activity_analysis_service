from uuid import UUID

from inflection import camelize
from functools import partial

from pydantic import Extra
from pydantic.main import BaseModel
from enum import Enum


class PyUUID(UUID):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not v:
            return None
        try:
            return UUID(v)
        except ValueError:
            raise ValueError("Invalid UUID")

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CommonModel(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        use_enum_values = True
        json_encoders = {PyUUID: str}


class CommonModelWithExtra(BaseModel):
    class Config:
        extra = Extra.allow


class CamelModel(CommonModel):
    """
    class configured to return fields in camelCase for all the child classes
    """

    def get_by_alias(self, alias):
        for field, details in self.__fields__.items():
            if details.alias == alias:
                return self.__getattribute__(field)
        raise AttributeError(f"'{self.__class__}' object has no attribute with alias '{alias}'")

    class Config:
        """
        Config to return fields as camelCase but keep using snake_case in dev
        """

        alias_generator = partial(camelize, uppercase_first_letter=False)
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        use_enum_values = True


class SuccessResponse(Enum):
    success: bool
