import os
import subprocess
import datetime

from telegram import Bot, Update
from telegram.ext import CommandHandler, run_async

from tg_bot import dispatcher, LOGGER, OWNER_ID, SUDO_USERS


# ================= CONFIG =================

DB_NAME = os.getenv("POSTGRES_DB", "tgbot")
DB_USER = os.getenv("POSTGRES_USER", "tgbot")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "oomb")
DB_HOST = os.getenv("DB_HOST", "db")   # docker-compose service name
DB_PORT = os.getenv("DB_PORT", "5432")

BACKUP_DIR = "/tmp"

# ==========================================


"""def dump_database():

    ##Creates a fresh PostgreSQL dump and returns file path.

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{BACKUP_DIR}/db_backup_{timestamp}.sql"

    cmd = [
        "pg_dump",
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        "-f",
        backup_path,
    ]

    subprocess.check_call(cmd)
    return backup_path

"""

def dump_database():
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_path = f"/tmp/db_backup_{timestamp}.sql"

    cmd = [
        "docker",
        "exec",
        "tgbot-db",
        "pg_dump",
        "-U", DB_USER,
        DB_NAME
    ]

    with open(backup_path, "wb") as f:
        subprocess.check_call(cmd, stdout=f)

    return backup_path

@run_async
def dbbackup(bot: Bot, update: Update):
    """
    /dbbackup command – admin only.
    """
    user = update.effective_user

    if user.id != OWNER_ID and user.id not in SUDO_USERS:
        update.effective_message.reply_text("❌ You are not authorized to use this command.")
        return

    update.effective_message.reply_text("⏳ Creating database backup, please wait...")

    try:
        LOGGER.info("Manual DB backup triggered by user %s", user.id)

        backup_file = dump_database()

        with open(backup_file, "rb") as f:
            bot.send_document(
                chat_id=user.id,
                document=f,
                filename=os.path.basename(backup_file),
                caption="📦 Database backup"
            )

        os.remove(backup_file)

        update.effective_message.reply_text("✅ Database backup completed and sent.")

        LOGGER.info("DB backup sent successfully")

    except Exception as e:
        LOGGER.exception("DB backup failed")
        update.effective_message.reply_text("❌ Database backup failed.")
        bot.send_message(
            chat_id=OWNER_ID,
            text=f"❌ DB backup failed:\n`{e}`",
            parse_mode="Markdown"
        )


# ================= HANDLER REGISTRATION =================

DBBACKUP_HANDLER = CommandHandler("dbbackup", dbbackup)

dispatcher.add_handler(DBBACKUP_HANDLER)


# ================= MODULE METADATA =================

__help__ = """
*Database Backup*
- /dbbackup: Create a fresh database backup and receive it in PM.
(Admin only)
"""

__mod_name__ = "DB Backup"
