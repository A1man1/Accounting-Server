import typing
from datetime import date
from typing import Optional
from datetime import datetime

from serviceHandling.Schema.BaseSchema import BaseSchema, BaseModel

from sqlalchemy.sql.functions import current_date, current_timestamp

class IDModelMixin(BaseModel):
    """
    Schema to return Id field for all model schemas.
    """
    id: Optional[int]


class ModifiedTimeModelMixin(BaseModel):
    """
    Model Mixin for created and updated timestamp information tables.
    """
    last_modified_at: Optional[datetime] = current_timestamp

class UserSchema(BaseSchema):
    company_id: Optional[int] 
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    


class UserSchemaCreate(UserSchema):
    """Create schema .

    Args:
        BaseSchemaBase (Model): Base model schema for  resources.
    """
    role_type: Optional[int] = 0
    permission:Optional[typing.List[int]] = []
    is_active:Optional[bool] = True
    passwd: Optional[str]
    registered_date:Optional[date] = current_date


class UserSchemaUpdate(UserSchema, ModifiedTimeModelMixin):
    """Update schema for app providers.

    Args:
        AppProviderBase (Model): Base model schema for AppProvider resources.
    """
    
    is_active:Optional[bool]
    permission:Optional[typing.List[int]]


class UserSchemaInDB(IDModelMixin, ModifiedTimeModelMixin, UserSchema):
    """AppProvider schema for DB structure.

    Args:
        IDModelMixin (Type[BaseModel]): ID mixin for db id field.
        ModifiedTimeModelMixin (Type[BaseModel]): Modified Time Model Mixin
        BaseSchema (Model): Base model schema for BaseSchema resources.
    """
    pass

class UserSchemaOut(UserSchemaInDB):...


class CompanyDetailSchema(BaseSchema):
    name: Optional[str]
    tax_type: Optional[str]
    company_tax_id: Optional[str]
    address: Optional[str]
    areacode: Optional[str]
    country: Optional[str]
    city: Optional[str]
    email: Optional[str]
    contact_number: Optional[typing.List[str]]

class compnaySchemaCreate(CompanyDetailSchema):
    """Create schema .

    Args:
        BaseSchemaBase (Model): Base model schema for  resources.
    """
    pass


class CompanySchemaUpdate(CompanyDetailSchema):
    """Update schema for app providers.

    Args:
        AppProviderBase (Model): Base model schema for AppProvider resources.
    """
    pass


class CompanySchemaInDB(IDModelMixin, ModifiedTimeModelMixin, CompanyDetailSchema):
    """AppProvider schema for DB structure.

    Args:
        IDModelMixin (Type[BaseModel]): ID mixin for db id field.
        ModifiedTimeModelMixin (Type[BaseModel]): Modified Time Model Mixin
        BaseSchema (Model): Base model schema for BaseSchema resources.
    """
    pass


class CompanySchemaOut(CompanySchemaInDB):
    pass



