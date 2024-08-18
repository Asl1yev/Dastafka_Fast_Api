from fastapi import APIRouter,Depends
from sqlalchemy.orm import scoped_session, sessionmaker

from schemas import SignUpModel,LoginModel
from models import User,Product,Order
from database import session,Base,engine
from fastapi import HTTPException,status
from werkzeug.security import generate_password_hash,check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
session = scoped_session(sessionmaker(bind=engine))


auth_router=APIRouter(
    prefix="/auth"
)


@auth_router.post("/signup",status_code=status.HTTP_201_CREATED)
async def signup(user:SignUpModel):
    db_email=session.query(User).filter(user.email==User.email).first()
    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with this email already exists")
    db_username=session.query(User).filter(user.username==User.username).first()
    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with this username already exists")


    new_user=User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active,
    )

    session.add(new_user)
    session.commit()

    data={
        "id":new_user.id,
        "username":new_user.username,
        "email":new_user.email,
        "is_staff":new_user.is_staff,
        "is_active":new_user.is_active,
    }

    response_model={
        "message":"Created successfully new user",
        "status":201,
        "data":data
    }
    return response_model

@auth_router.post('/login',status_code=status.HTTP_200_OK)
async def login(user:LoginModel,Authorize:AuthJWT=Depends()):
    db_user=session.query(User).filter(user.username==User.username).first()
    if db_user and check_password_hash(db_user.password,user.password):
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid username or password")
        access_token=Authorize.create_access_token(subject=db_user.username)
        refresh_token=Authorize.create_refresh_token(subject=db_user.username)

        data={
            'message':'Succwssfully user login',
            "status":'status.HTTP_200_OK',
            'token':{
                'access':access_token,
                'refresh':refresh_token,
            }
        }

        return jsonable_encoder(data)