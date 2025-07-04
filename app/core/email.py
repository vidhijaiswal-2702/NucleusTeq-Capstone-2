# import os
# from pathlib import Path
# from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
# from fastapi.background import BackgroundTasks
# from app.core.settings import get_settings

# settings = get_settings()

# conf = ConnectionConfig(
#     MAIL_USERNAME="",  # Mailpit doesn't require username/password
#     MAIL_PASSWORD="",
#     MAIL_PORT=int(os.environ.get("MAIL_PORT", 1025)),
#     MAIL_SERVER=os.environ.get("MAIL_SERVER", "localhost"),  # Must be localhost for Mailpit
#     MAIL_STARTTLS=False,
#     MAIL_SSL_TLS=False,
#     MAIL_DEBUG=True,
#     MAIL_FROM=os.environ.get("MAIL_FROM", "noreply@test.com"),
#     MAIL_FROM_NAME=os.environ.get("MAIL_FROM_NAME", settings.APP_NAME),
#     TEMPLATE_FOLDER=Path("app/auth/templates"),
#     USE_CREDENTIALS=False,
# )

# fm = FastMail(conf)


# async def send_email(recipients: list, subject: str, context: dict, template_name: str,
#                      background_tasks: BackgroundTasks):
#     message = MessageSchema(
#         subject=subject,
#         recipients=recipients,
#         template_body=context,
#         subtype=MessageType.html
#     )

#     background_tasks.add_task(fm.send_message, message, template_name=template_name)

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from fastapi.background import BackgroundTasks
from app.core.settings import get_settings
from pathlib import Path
from typing import List

settings = get_settings()

# Mailpit configuration (for local development)
mailpit_conf = ConnectionConfig(
    MAIL_USERNAME="",
    MAIL_PASSWORD="",
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    MAIL_DEBUG=True,
    TEMPLATE_FOLDER=Path("app/auth/templates"),
    USE_CREDENTIALS=settings.USE_CREDENTIALS
)

# Real SMTP configuration (e.g. Gmail)
realmail_conf = ConnectionConfig(
    MAIL_USERNAME=settings.REAL_MAIL_USERNAME,
    MAIL_PASSWORD=settings.REAL_MAIL_PASSWORD,
    MAIL_PORT=settings.REAL_MAIL_PORT,
    MAIL_SERVER=settings.REAL_MAIL_SERVER,
    MAIL_FROM=settings.REAL_MAIL_FROM,
    MAIL_FROM_NAME=settings.REAL_MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.REAL_MAIL_TLS,
    MAIL_SSL_TLS=False,
    MAIL_DEBUG=True,
    TEMPLATE_FOLDER=Path("app/auth/templates"),
    USE_CREDENTIALS=True
)


async def send_email(
    recipients: List[str],
    subject: str,
    context: dict,
    template_name: str,
    background_tasks: BackgroundTasks,
    use_real_smtp: bool = False
) -> None:
    """
    Send an email via Mailpit (dev) or Gmail SMTP (prod) depending on `use_real_smtp` flag.

    Args:
        recipients (List[str]): List of recipient email addresses.
        subject (str): Email subject.
        context (dict): Template context.
        template_name (str): Path to the HTML template.
        background_tasks (BackgroundTasks): FastAPI BackgroundTasks object.
        use_real_smtp (bool): Whether to use real SMTP (Gmail). Defaults to False.
    """
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=context,
        subtype=MessageType.html
    )

    conf = realmail_conf if use_real_smtp and settings.REAL_MAIL_ENABLED else mailpit_conf
    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message, template_name=template_name)
