from typing import Any, List , Dict , Optional

from requests.models import CaseInsensitiveDict


from core.config import log
import json
from serviceHandling.Schema import util
from fastapi import APIRouter, Depends, HTTPException, Security, status
from serviceHandling.Schema.modelAcess.login import LoginOut , UserLoginSchema
from serviceHandling.security.authentication import JWTBearer
from starlette.status import HTTP_204_NO_CONTENT, HTTP_406_NOT_ACCEPTABLE
from serviceHandling.Eventhandling.events import session
from core.config import settings
from AiModule.utils import Util
from ..Schema.modelAcess.invoice import InvoiceSchema, InvoiceSchemaCreate , InvoiceSchemaOut
from ..Schema.ModelOpreation.billing import InvoiceRepository

router = APIRouter(
    prefix="/billing",
    tags=["Billing"]
)


headers= CaseInsensitiveDict()
auth:JWTBearer=JWTBearer(100)
util_func:Util = Util()
resp:InvoiceRepository = InvoiceRepository()


@router.post('/billing_perpare',name="Billing Prepare api", response_model=InvoiceSchemaOut)
async def perpare_bill(data:InvoiceSchemaCreate, dependencies=Depends(auth)):
    """[summary]

    Args:
        data (InvoiceSchema): [description]
        dependencies ([type], optional): [description]. Defaults to Depends(auth).

    Returns:
        [type]: [description]
    """
    try:    
            if data:
                return await resp.create(data)
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="empty data has no addition!")

    except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=[err.detail])
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
