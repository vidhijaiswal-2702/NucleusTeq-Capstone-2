from datetime import datetime, timedelta
import logging
from app.auth.models import User, UserToken
from app.auth.schemas import ResetPasswordRequest
from app.core.logger import get_logger
from sqlalchemy.orm import joinedload ,Session # type: ignore
from app.auth.utils.email_context import FORGOT_PASSWORD, USER_VERIFY_ACCOUNT
from app.auth.utils.string import unique_string
from app.core import settings
from app.core.security import generate_token, get_token_payload, hash_password, is_password_strong_enough, load_user, str_decode, str_encode, verify_password
from sqlalchemy.exc import IntegrityError  # type: ignore
from fastapi import HTTPException, status, BackgroundTasks  # type: ignore
from app.auth.emailService import send_account_activation_confirmation_email, send_account_verification_email, send_password_reset_email
import secrets
from datetime import datetime, timedelta
from app.auth.models import PasswordResetToken

settings = settings.get_settings()
logger = get_logger("auth")


async def create_user(data, session, background_tasks):
    logger.info(f"Attempting to register user: {data.email}")
    if not is_password_strong_enough(data.password):
        raise HTTPException(status_code=400,
                            detail="Password must be at least 8 characters long, "
                                   "contain at least one uppercase letter, one lowercase letter, "
                                   "one digit, and one special character.")

    if not data.name:
        raise HTTPException(status_code=400, detail="Name is mandatory.")

    if not data.email:
        raise HTTPException(status_code=400, detail="Email is mandatory.")

    if not data.role.value:
        raise HTTPException(status_code=400, detail="Please select a valid role.")

    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=data.role.value,
        is_active=False,
        updated_at=datetime.utcnow()
    )
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        logger.warning(f"Registration failed - Email already registered: {data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    session.refresh(user)
    logger.info(f"User registered successfully: {user.email}")
    await send_account_verification_email(user, background_tasks=background_tasks)
    return user


async def activate_user(data, session, background_tasks):
    logger.info(f"Attempting account activation for: {data.email}")
    user = session.query(User).filter(User.email == data.email).first()
    if not user:
        logger.warning(f"Activation failed - Email not found: {data.email}")
        raise HTTPException(
            status_code=400,
            detail="The link is not valid."
        )
    user_token = user.get_context_string(context=USER_VERIFY_ACCOUNT) #generate a secure token based on user state

    try:
        token_valid = verify_password(user_token, data.token) #Compare it with token from the email link
    except Exception as verify_exec:
        logging.exception(verify_exec)
        token_valid = False

    if not token_valid:
        logger.warning(f"Activation failed - Invalid token for user: {user.email}")
        raise HTTPException(
            status_code=400,
            detail="The link is either expired or not valid."
        )
        #if token valid 
    user.is_active = True
    user.updated_at = datetime.utcnow()
    user.verified_at = datetime.utcnow()
    session.add(user)
    session.commit()
    session.refresh(user)
    logger.info(f"User activated successfully: {user.email}")
    await send_account_activation_confirmation_email(user, background_tasks) #send welcome email after activation
    return user


async def get_login_token(data, session):
    logger.info(f"Login attempt for: {data.username}")
    user = await load_user(data.username, session) # load_user is a utility func to fetch user by email 
    if not user:
        logger.warning(f"Login failed - Email not found: {data.username}")
        raise HTTPException(status_code=400, detail="Email is not registered.")

    if not verify_password(data.password, user.password):
        logger.warning(f"Login failed - Invalid credentials for: {data.username}")
        raise HTTPException(status_code=400, detail="Invalid email or password.")

    if not user.verified_at:
        logger.warning(f"Login failed - Account not verified: {user.email}")
        raise HTTPException(status_code=400, detail="Your account is not verified. Please check your email for the verification link.")

    if not user.is_active:
        logger.warning(f"Login failed - Account inactive: {user.email}")
        raise HTTPException(status_code=400, detail="Your account is not active.")

    logger.info(f"Login successful for: {user.email}")
    return _generate_tokens(user, session)  #generate access and refresh tokens for the user


async def get_refresh_token(refresh_token, session):
    logger.info(f"Refresh token requested.")   # Called when access token expires. Validates refresh token & issues new tokens.
    
    token_payload = get_token_payload(refresh_token, settings.SECRET_KEY, settings.JWT_ALGORITHM)  #get_token_payload is a utility function to decode the token and extract payload
    if not token_payload:
        logger.warning("Invalid refresh token payload.")
        raise HTTPException(status_code=400, detail="Invalid Request.")

    refresh_key = token_payload.get('t')
    access_key = token_payload.get('a')
    user_id = str_decode(token_payload.get('sub'))

    user_token = session.query(UserToken).options(joinedload(UserToken.user)).filter( #joins usertoken and users table to look for token
        UserToken.refresh_key == refresh_key, 
        UserToken.access_key == access_key,
        UserToken.user_id == user_id,
        UserToken.expires_at > datetime.utcnow()
    ).first()

    if not user_token:
        logger.warning(f"Refresh token failed - Token not found or expired.")
        raise HTTPException(status_code=400, detail="Invalid Request.")

    user_token.expires_at = datetime.utcnow()
    session.add(user_token)
    session.commit()
    logger.info(f"Refresh token successful for user: {user_token.user.email}")
    return _generate_tokens(user_token.user, session)


def _generate_tokens(user, session):
    refresh_key = unique_string(100)
    access_key = unique_string(50)
    rt_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    user_token = UserToken()
    user_token.user_id = user.id
    user_token.refresh_key = refresh_key
    user_token.access_key = access_key
    user_token.expires_at = datetime.utcnow() + rt_expires
    session.add(user_token)
    session.commit()
    session.refresh(user_token)

    at_payload = {      #create jwt access tokens 
        "sub": str_encode(str(user.id)),
        'a': access_key,
        'r': str_encode(str(user_token.id)),
        'n': str_encode(f"{user.name}"),
        'role': user.role
    }

    at_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_token(at_payload, settings.JWT_SECRET, settings.JWT_ALGORITHM, at_expires)

    rt_payload = {"sub": str_encode(str(user.id)), "t": refresh_key, 'a': access_key} # create jwt refresh tokens
    refresh_token = generate_token(rt_payload, settings.SECRET_KEY, settings.JWT_ALGORITHM, rt_expires)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": at_expires.seconds
    }



async def forgot_password_link(data, background_tasks, session):
    logger.info(f"Password reset requested for: {data.email}")
    user = await load_user(data.email, session)

    if not user:
        logger.warning(f"Password reset request for non-existent user: {data.email}")
        return

    if not user.verified_at:
        raise HTTPException(status_code=400, detail="Account not verified.")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account not active.")

    # 1. Generate token
    token = secrets.token_urlsafe(32)

    # 2. Create token object
    token_obj = PasswordResetToken(
        user_id=user.id,
        token=token,
        expiration_time=datetime.utcnow() + timedelta(minutes=15),
        used=False
    )

    session.add(token_obj)
    session.commit()

    # 3. Send email (update send_password_reset_email to accept token)
    await send_password_reset_email(user,  background_tasks,session)

    logger.info(f"Password reset token saved and email sent to: {user.email}")



async def reset_user_password(data: ResetPasswordRequest, session):
    logger.info(f"Password reset attempt for: {data.email}")
    user = await load_user(data.email, session)

    if not user or not user.verified_at or not user.is_active:
        raise HTTPException(status_code=400, detail="Invalid Request.")

    # Lookup the token
    token_entry = session.query(PasswordResetToken).filter_by(
        user_id=user.id,
        token=data.token,
        used=False
    ).first()

    if not token_entry or token_entry.expiration_time < datetime.utcnow():
        logger.warning(f"Password reset failed - Invalid/expired token for: {user.email}")
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    # Update password
    user.password = hash_password(data.password)
    user.updated_at = datetime.utcnow()

    # Mark token as used
    token_entry.used = True
    session.add_all([user, token_entry])
    session.commit()
    session.refresh(user)

    logger.info(f"Password reset successful for: {user.email}")
    return {"message": "Your password has been updated successfully."}



async def logout_service(current_user: User, session: Session):
    logger.info(f"Logout attempt for: {current_user.email}")

    try:
        tokens = session.query(UserToken).filter(UserToken.user_id == current_user.id).all()
        if not tokens:
            logger.warning(f"No active tokens found for user: {current_user.email}")
        else:
            for token in tokens:
                session.delete(token)
            session.commit()
            logger.info(f"User logged out successfully: {current_user.email}")
        return {"detail": "Logout successful."}
    except Exception as e:
        logger.error(f"Logout failed for user {current_user.email}: {str(e)}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Logout failed. Please try again.")
