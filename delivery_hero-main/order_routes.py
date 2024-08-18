from fastapi import  ApiRouter
from fastapi import APIRouter,Depends
from sqlalchemy.orm import scoped_session, sessionmaker

from schemas import SignUpModel,LoginModel
from models import User,Product,Order
from database import session,Base,engine
from fastapi import HTTPException,status
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

order_ruters=ApiRouter(
    prefix='/order'
)
