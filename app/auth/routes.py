
from email.header import Header
from app.auth.models import User
from app.auth.schemas import EmailRequest, LoginResponse, RegisterUserRequest, ResetPasswordRequest, UserResponse, VerifyUserRequest
from app.auth.services import activate_user, create_user,  forgot_password_link, get_login_token, get_refresh_token, logout_service, reset_user_password
from app.core.database import get_session
from fastapi import APIRouter, Depends # type: ignore
from sqlalchemy.orm import Session # type: ignore
from fastapi import status, BackgroundTasks ,Request# type: ignore
from fastapi.security import OAuth2PasswordRequestForm # type: ignore
from app.core.security import oauth2_scheme, get_current_user


user_router = APIRouter(    # register user,verify user
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)
auth_router = APIRouter(        # retieve current user details 
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme), Depends(get_current_user)]
)
guest_router = APIRouter(  # login,logout,forgot pass, reset pass
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

@user_router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(data: RegisterUserRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
   return await create_user(data, session, background_tasks) #send verification email after user registration

@user_router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_user(data: VerifyUserRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
   return await activate_user(data, session, background_tasks) #send welcome mail after verification

"""
    Send welcome mail after verification
    """

@guest_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login_user(
    data: OAuth2PasswordRequestForm = Depends(),  
    session: Session = Depends(get_session)
):
    return await get_login_token(data, session)

@guest_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def refresh_tokens(refresh_token = Header(),  session: Session = Depends(get_session)):
    return await get_refresh_token(refresh_token, session)

@guest_router.post("/forgot-password",status_code=status.HTTP_200_OK)
async def forgot_password(data: EmailRequest,background_tasks:BackgroundTasks,session:Session = Depends(get_session)): 
    await forgot_password_link(data,background_tasks,session)
    return {"message": "If the email is registered, a reset link has been sent."} #send reset link to the email if it exists

@guest_router.post("/reset-password",status_code=status.HTTP_200_OK)
async def reset_password(data: ResetPasswordRequest,session:Session = Depends(get_session)): 
    await reset_user_password(data,session)
    return {"Your password hase been updated successfully."}

@guest_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(
    request: Request,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)  
):
    return await logout_service(current_user, session) # delete access and refresh tokens for the user


@auth_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def fetch_user(user = Depends(get_current_user)):
    """
    Retrieves current user details
    """
    return user

