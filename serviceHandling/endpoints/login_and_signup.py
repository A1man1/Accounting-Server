import json

from AiModule.utils import Util
from core.config import log, settings
from fastapi import APIRouter, HTTPException, status
from requests.models import CaseInsensitiveDict
from serviceHandling.Eventhandling.events import session
from serviceHandling.Schema.modelAcess.login import LoginOut, UserLoginSchema 
from serviceHandling.Schema.modelAcess.user import CompanySchemaOut, UserSchemaCreate, UserSchemaOut, compnaySchemaCreate
from serviceHandling.security.authentication import JWTBearer

from ..Schema.ModelOpreation.billing import InvoiceRepository

router = APIRouter(
    prefix="/authentication",
    tags=["Authorization"]
)


headers= CaseInsensitiveDict()
auth:JWTBearer=JWTBearer(100)
util_func:Util = Util()
resp:InvoiceRepository = InvoiceRepository()

@router.post('/login',name='login erp system',response_model=LoginOut)
async def login(data:UserLoginSchema):
    """[summary]

    Args:
        username (str): [description]
        password (str): [description]

    Returns:
        [type]: [description]
    """
    try:

        url=settings.base_url.__add__('/api/v1/users/authenticate/')
        data=dict(data)
        print(json.dumps(data))
        response = session.post(url=url,headers=headers,data=json.dumps(data))    
        return response.json()
    
    except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=[err.detail])
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.post('/signup', name='sign up erp system',response_model=UserSchemaOut)
async def signup(data:UserSchemaCreate):
    """[summary]

    Args:
        username (str): [description]
        password (str): [description]

    Returns:
        [type]: [description]
    """
    try:

        url=settings.base_url.__add__('/api/v1/users/')
        data=dict(data)
        print(json.dumps(data))
        response = session.post(url=url,headers=headers,data=json.dumps(data))    
        return response.json()
    
    except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=[err.detail])
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.post('/signup', name='sign up erp system',response_model=UserSchemaOut)
async def signup(data:UserSchemaCreate):
    """[summary]

    Args:
        username (str): [description]
        password (str): [description]

    Returns:
        [type]: [description]
    """
    try:

        url=settings.base_url.__add__('/api/v1/users/')
        data=dict(data)
        print(json.dumps(data))
        response = session.post(url=url,headers=headers,data=json.dumps(data))    
        return response.json()
    
    except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=[err.detail])
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.post('/company', name='create in erp system',response_model=CompanySchemaOut)
async def signup(data:compnaySchemaCreate):
    """[summary]

    Args:
        username (str): [description]
        password (str): [description]

    Returns:
        [type]: [description]
    """
    try:

        url=settings.base_url.__add__('/api/v1/company/')
        data=dict(data)
        print(json.dumps(data))
        response = session.post(url=url,headers=headers,data=json.dumps(data))    
        return response.json()
    
    except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=[err.detail])
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")



