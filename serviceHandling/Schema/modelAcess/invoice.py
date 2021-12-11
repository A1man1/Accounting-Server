import enum
import typing
from typing import Any, Dict, Optional
from datetime import  datetime
from serviceHandling.Schema.BaseSchema import (BaseSchema, IDModelMixin, DateTimeModelMixin, CreateDateTime , UpdateDateTime)
from serviceHandling.Schema.modelAcess.product import ProductSchema
from pydantic import Field

class InvoiceSchema(BaseSchema):
    name: Optional[str]
    tax_type: Optional[str]
    company_tax_id: Optional[str]
    address: Optional[str]
    areacode: Optional[str]
    country: Optional[str]
    city: Optional[str]
    email: Optional[str]
    contact_number: Optional[typing.List[str]]

    #suppiler
    suppiler_name:Optional[str]
    suppiler_company_tax_id: Optional[str]
    suppiler_address: Optional[str]
    suppiler_areacode: Optional[str]
    suppiler_country: Optional[str]
    suppiler_city: Optional[str]
    suppiler_email: Optional[str]
    suppiler_contact_number: Optional[typing.List[str]]

    #core mode date 
    invoice_number:Optional[str]
    invoice_date:Optional[datetime]= Field(..., alias="invoice_date")
    invoice_p_o_number:Optional[str]
    transport_mode:Optional[str]
    vechicle_no:Optional[str]

    #product
    product_data:Optional[typing.List[Dict[Any,Any]]]= Field(default_factory=ProductSchema,alias='products')



class InvoiceSchemaCreate(InvoiceSchema):
    """Create schema .

    Args:
        BaseSchemaBase (Model): Base model schema for  resources.
    """
    created_at: Optional[datetime] = Field(..., alias="created_at")
    updated_at: Optional[datetime] = None


class InvoiceSchemaUpdate(InvoiceSchema):
    """Update schema for app providers.

    Args:
        AppProviderBase (Model): Base model schema for AppProvider resources.
    """
    updated_at: Optional[datetime] = Field(...,alias="updated_at")


class InvoiceSchemaInDB(IDModelMixin, DateTimeModelMixin, InvoiceSchema):
    """AppProvider schema for DB structure.

    Args:
        IDModelMixin (Type[BaseModel]): ID mixin for db id field.
        ModifiedTimeModelMixin (Type[BaseModel]): Modified Time Model Mixin
        BaseSchema (Model): Base model schema for BaseSchema resources.
    """
    pass


class InvoiceSchemaOut(InvoiceSchemaInDB):
    pass



