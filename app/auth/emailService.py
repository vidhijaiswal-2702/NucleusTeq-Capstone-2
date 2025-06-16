from fastapi import BackgroundTasks
from app.core.settings import get_settings
from app.auth.models import User, PasswordResetToken
from app.core.email import send_email
from app.auth.utils.email_context import FORGOT_PASSWORD, USER_VERIFY_ACCOUNT
import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

settings = get_settings()


async def send_account_verification_email(user: User, background_tasks: BackgroundTasks):
    from app.core.security import hash_password
    string_context = user.get_context_string(context=USER_VERIFY_ACCOUNT)
    token = hash_password(string_context)
    activate_url = f"{settings.FRONTEND_HOST}/auth/account-verify?token={token}&email={user.email}"
    data = {
        'app_name': settings.APP_NAME,
        "name": user.name,
        'activate_url': activate_url
    }
    subject = f"Account Verification - {settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="user/account-verification.html",
        context=data,
        background_tasks=background_tasks,
        #use_real_smtp=True 
    )
    
    
async def send_account_activation_confirmation_email(user: User, background_tasks: BackgroundTasks):
    data = {
        'app_name': settings.APP_NAME,
        "name": user.name,
        'login_url': f'{settings.FRONTEND_HOST}'
    }
    subject = f"Welcome - {settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="user/account-verification-confirmation.html",
        context=data,
        background_tasks=background_tasks,
        #use_real_smtp=True
    )
    
async def send_password_reset_email(user: User, background_tasks: BackgroundTasks, session: Session):
    # 1. Generate a secure token
    token = secrets.token_urlsafe(32)

    # 2. Store it in the database
    expiration_time = datetime.utcnow() + timedelta(minutes=15)

    reset_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expiration_time=expiration_time,
        used=False
    )

    session.add(reset_token)
    session.commit()

    # 3. Generate the reset URL with the token and email
    reset_url = f"{settings.FRONTEND_HOST}/reset-password?token={token}&email={user.email}"

    # 4. Email content
    data = {
        'app_name': settings.APP_NAME,
        "name": user.name,
        'activate_url': reset_url,
    }

    subject = f"Reset Password - {settings.APP_NAME}"

    await send_email(
    recipients=[user.email],
    subject=subject,
    template_name="user/password-reset.html",
    context=data,
    background_tasks=background_tasks,
    use_real_smtp=True 
)
    