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
    prefix="/maths_utils",
    tags=["Maths"]
)

headers= CaseInsensitiveDict()
auth:JWTBearer=JWTBearer(100)
util_func:Util = Util()
resp:InvoiceRepository = InvoiceRepository()

@router.post("/addition/",name="Total Addition of list") 
async def get_total_addition(data:List[float], dependencies=Depends(auth)):
    """[summary]

    Args:
        data (List[float]): [description]
        dependencies ([type], optional): [description]. Defaults to Depends(auth).

    Raises:
        HTTPException: [description]
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    try:    
            #token=dependencies['token']
            #headers['Authorization']= f'Bearer {token}'
            #url=settings.base_url.__add__('/api/v1/product/company/')
            #companys = session.get(url=url,headers=headers,data=data)
            #if companys.status_code == 200 :
            #   return companys.json()
            if data:
                
                return  {'total_addition':util_func.big_float_addition(data)}
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="empty data has no addition!")

    except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=[err.detail])
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")
       

@router.post("/average/",name="average of list integer") 
async def get_total_addition(data:List[float], dependencies=Depends(auth)):
    """[summary]

    Args:
        data (List[float]): [description]
        dependencies ([type], optional): [description]. Defaults to Depends(auth).

    Raises:
        HTTPException: [description]
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    try:    
            #token=dependencies['token']
            #headers['Authorization']= f'Bearer {token}'
            #url=settings.base_url.__add__('/api/v1/product/company/')
            #companys = session.get(url=url,headers=headers,data=data)
            #if companys.status_code == 200 :
            #   return companys.json()
            if data:
                return  {'avreage':util_func.big_float_average(data)}
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="empty data has no addition!")

    except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=[err.detail])
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.post("/subtraction/",name="Subtraction of integer or float") 
async def get_total_addition(data1:float,data2:float, dependencies=Depends(auth)):
    """[summary]

    Args:
        data (List[float]): [description]
        dependencies ([type], optional): [description]. Defaults to Depends(auth).

    Raises:
        HTTPException: [description]
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    try:    
            #token=dependencies['token']
            #headers['Authorization']= f'Bearer {token}'
            #url=settings.base_url.__add__('/api/v1/product/company/')
            #companys = session.get(url=url,headers=headers,data=data)
            #if companys.status_code == 200 :
            #   return companys.json()
            if data1 and data2:
                return  {'avreage':util_func.big_float_subtraction(data1,data2)}
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="empty data has no addition!")

    except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=[err.detail])
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.post("/divide/",name="divide of integer or float") 
async def get_total_addition(data1:float,data2:float, dependencies=Depends(auth)):
    """[summary]

    Args:
        data (List[float]): [description]
        dependencies ([type], optional): [description]. Defaults to Depends(auth).

    Raises:
        HTTPException: [description]
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    try:    
            #token=dependencies['token']
            #headers['Authorization']= f'Bearer {token}'
            #url=settings.base_url.__add__('/api/v1/product/company/')
            #companys = session.get(url=url,headers=headers,data=data)
            #if companys.status_code == 200 :
            #   return companys.json()
            if data1 and data2:
                return  {'avreage':util_func.big_float_subtraction(data1,data2)}
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="empty data has no addition!")

    except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=[err.detail])
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.post("/dividmod/",name="dividmod of integer or float") 
async def get_total_addition(data1:float,data2:float, dependencies=Depends(auth)):
    """[summary]

    Args:
        data (List[float]): [description]
        dependencies ([type], optional): [description]. Defaults to Depends(auth).

    Raises:
        HTTPException: [description]
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    try:    
            #token=dependencies['token']
            #headers['Authorization']= f'Bearer {token}'
            #url=settings.base_url.__add__('/api/v1/product/company/')
            #companys = session.get(url=url,headers=headers,data=data)
            #if companys.status_code == 200 :
            #   return companys.json()
            if data1 and data2:
                return  {'avreage':util_func.big_float_divmod(data1,data2)}
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="empty data has no addition!")

    except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=[err.detail])
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


@router.post("/Multiplication/",name="Multiplication of integer or float") 
async def get_total_addition(data1:List[float] ,data2:List[float], dependencies=Depends(auth)):
    """[summary]

    Args:
        data (List[float]): [description]
        dependencies ([type], optional): [description]. Defaults to Depends(auth).

    Raises:
        HTTPException: [description]
        HTTPException: [description]
        HTTPException: [description]

    Returns:
        [type]: [description]
    """
    try:    
            #token=dependencies['token']
            #headers['Authorization']= f'Bearer {token}'
            #url=settings.base_url.__add__('/api/v1/product/company/')
            #companys = session.get(url=url,headers=headers,data=data)
            #if companys.status_code == 200 :
            #   return companys.json()
            if data1 and data2:
                return  {'avreage':util_func.big_float_multipilcaiton(data1,data2)}
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="empty data has no addition!")

    except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=[err.detail])
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")