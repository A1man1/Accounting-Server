from typing import  Type
from serviceHandling.Schema.BaseSchema import BaseRepository , Collections
from serviceHandling.Schema.modelAcess.invoice import  InvoiceSchemaCreate , InvoiceSchemaOut, InvoiceSchemaUpdate


class InvoiceRepository(BaseRepository):

    @property
    def _db_collection(self):
        return Collections.invoice_collection

    @property
    def _schema_out(self) -> Type[InvoiceSchemaOut]:
        return InvoiceSchemaOut

    @property
    def _schema_create(self) -> Type[InvoiceSchemaCreate]:
        return InvoiceSchemaCreate

    @property
    def _schema_update(self) -> Type[InvoiceSchemaUpdate]:
        return InvoiceSchemaUpdate
