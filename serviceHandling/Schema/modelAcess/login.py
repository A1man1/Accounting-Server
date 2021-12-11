from serviceHandling.Schema.BaseSchema import BaseSchema

class UserLoginSchema(BaseSchema):
    email:str
    passd:str

class LoginOut(BaseSchema):
     access_token:str