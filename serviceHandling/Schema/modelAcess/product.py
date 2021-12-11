import enum
import typing
from typing import Optional
from datetime import date
from serviceHandling.Schema.BaseSchema import (BaseSchema, IDModelMixin,
                                    DateTimeModelMixin)


class ProductSchema(BaseSchema):
    product_name: Optional[str] 
    product_number: Optional[str]
    product_label: Optional[str]
    price:Optional[float]
    quantity:Optional[int]
    


class ProductSchemCreate(ProductSchema):
    """Create schema .

    Args:
        BaseSchemaBase (Model): Base model schema for  resources.
    """
    pass


class ProductSchemUpdate(ProductSchema):
    """Update schema for app providers.

    Args:
        AppProviderBase (Model): Base model schema for AppProvider resources.
    """
    pass


class ProductSchemaInDB(IDModelMixin, DateTimeModelMixin , ProductSchema):
    """AppProvider schema for DB structure.

    Args:
        IDModelMixin (Type[BaseModel]): ID mixin for db id field.
        ModifiedTimeModelMixin (Type[BaseModel]): Modified Time Model Mixin
        BaseSchema (Model): Base model schema for BaseSchema resources.
    """
    pass


class ProductSchemaOut(ProductSchemaInDB):
    pass



