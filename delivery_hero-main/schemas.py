from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id:Optional[int]
    username :str
    email :str
    password:Optional[str]
    is_staff:Optional[bool]
    is_active:Optional[bool]

    class Config:
        from_attributes=True
        json_schema_extra ={
            "example":{
                "username":"eshmat",
                "email":"eshmat@gmail.com",
                "password":"eshmat123",
                "is_staff":False,
                "is_active":True,

            }
        }


class LoginModel(BaseModel):
    username:str
    password:str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "eshmat",
                "password": "eshmat123",

            }
        }

class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str]="PENDING"
    user_id:Optional[int]

    class Config:
        from_attributers=True
        json_schema_extra={
            "example":{
                'id':1,
                "quantity":1,
                'order_status':"PENDING",
                'user_id':1
            }
        }



class Settings(BaseModel):
    authjwt_secret_key:str="25d4208f5355be31b70f1d2c81239df92198d95e9ed42d879348cf267e50390d"