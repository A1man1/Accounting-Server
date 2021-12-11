import time

import jwt
from fastapi import  HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.config import log
from serviceHandling.security.permisison.permission import _Schema_Admin

from core.settings import Settings


class AuthHandler:

    
    def __init__(self):
         pass
        
    
    async def token_response(self,token: str):
        return {
            "access_token": token
        }

        
    async def verify(self, token:str)->dict:
        """Decode JWT token to check for permission.

        Args:
            token (str): Auth token for user.
        """

        try:
                user = jwt.decode(token, key=Settings().secret_key, algorithms=Settings().algorithm)
                
                if  not user["is_active"] and user["role_type"] is not None:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Deactivated User Account")
                if user['expires'] < time.time():
                    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="token Invaild") 
                
                return user

        except jwt.ExpiredSignatureError as sign_err:
            log.warn(sign_err)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature has expired")

        except jwt.InvalidTokenError as token_err:
            log.warn(token_err)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")

        except Exception as err:
            log.error(err)
            if hasattr(err, 'status_code'):
                raise HTTPException(status_code=err.status_code, detail=err.detail)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error Msg: { err }")


class JWTBearer(HTTPBearer, AuthHandler,_Schema_Admin):
    def __init__(self, permission_type:int ,auto_error: bool = True):
        self.permission = permission_type
        self.super_admin= ord(self.admin_permit())
        super(AuthHandler,self).__init__()
        super(JWTBearer, self).__init__(auto_error=auto_error,scheme_name='Authorization')

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            verify = await self.verify_jwt(credentials.credentials)
            if not verify:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")    
            user_permissions = verify['permission']

            name , email , company_id =  None , verify['email'] , verify['company_id'] 
            try:
                first = verify['first_name']
                middle= verify['middle_name']
                last =  verify['last_name']
                name = first+" "+middle+' '+last
            except:
                first = verify['first_name']
                middle= ""
                last =  verify['last_name']
                name = first+" "+last
            data={'name':name,'email':email,'company_id':company_id, 'token': credentials.credentials}

            if not self.permission in user_permissions or\
              not int(self.super_admin) in user_permissions and\
                   self.permission == int(self.super_admin):
                raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="contact to admin to access this action!")
            return data
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    async def verify_jwt(self, jwtoken: str) -> dict:
        return await self.verify(jwtoken)
