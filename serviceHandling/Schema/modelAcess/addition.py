import enum
import typing
from typing import Optional

from serviceHandling.Schema.BaseSchema import (BaseSchema, IDModelMixin,
                                    ModifiedTimeModelMixin)


class AdditionSchema(BaseSchema):
    total_addition: float

class AdditionSchemaCreate(AdditionSchema):
    """Create schema .

    Args:
        BaseSchemaBase (Model): Base model schema for  resources.
    """
    pass


class AdditionSchemaUpdate(AdditionSchema):
    """Update schema for app providers.

    Args:
        AppProviderBase (Model): Base model schema for AppProvider resources.
    """
    pass


class AdditionSchemaInDB(IDModelMixin, ModifiedTimeModelMixin, AdditionSchema):
    """AppProvider schema for DB structure.

    Args:
        IDModelMixin (Type[BaseModel]): ID mixin for db id field.
        ModifiedTimeModelMixin (Type[BaseModel]): Modified Time Model Mixin
        BaseSchema (Model): Base model schema for BaseSchema resources.
    """
    pass


class AdditionSchemaOut(AdditionSchemaInDB):
    pass



