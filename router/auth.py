from schemas.user import User
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from fastapi import APIRouter, status
 
auth_router =  APIRouter()

@auth_router.post("/login", tags=['auth'], response_model=dict, status_code=status.HTTP_200_OK)
def login(user: User):
    if user.email == "admin@mail.com" and user.password == "admin":
        token = create_token(data=user.model_dump())
        result = JSONResponse(content={"token":token},
                              status_code=status.HTTP_200_OK)
    else:
        result = JSONResponse(content={"message": "Invalid credentials"},
                              status_code=status.HTTP_401_UNAUTHORIZED)
    return result
