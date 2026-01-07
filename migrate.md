# 🚀 Telegram Bot Migration Guide (Docker + PostgreSQL)

This guide walks you **step by step** through migrating your **Telegram bot + Dockerized PostgreSQL database**  
from one VPS/server to another **safely and cleanly**.

It is written so you can follow it **line by line** without guessing.

---

## 🧭 Migration Overview

What will be migrated:

- ✅ Bot source code
- ✅ Docker setup (`Dockerfile`, `docker-compose.yml`)
- ✅ PostgreSQL database (via `pg_dump`)
- ✅ Environment variables & configs

What will **NOT** be migrated directly:

- ❌ Docker volumes
- ❌ `/var/lib/docker`
- ❌ System PostgreSQL on the VPS

---

## 🧱 Current Architecture (Source Server)

```
VPS
 └── Docker
     ├── legacy-tgbot  (Python bot container)
     └── tgbot-db      (PostgreSQL container)
```

Database data lives inside a **Docker volume**, not on the VPS directly.

---

## 📋 Prerequisites (Before You Start)

On **both servers**:

- Ubuntu 20.04 / 22.04
- Docker installed
- Docker Compose available
- SSH access

---

## 🔹 STEP 1: Take a Database Backup (Source Server)

Run this on the **OLD server**:

```bash
docker exec tgbot-db pg_dump -U tgbot tgbot > tgbot_backup.sql
```

Verify the backup:

```bash
ls -lh tgbot_backup.sql
```

✔ Ensure the file size is **not zero**

---

## 🔹 STEP 2: Archive Bot Project Files

From the bot project directory (`~/tgbot`):

```bash
tar -czvf tgbot_project.tar.gz   docker-compose.yml   Dockerfile   requirements.txt   tg_bot   Procfile   runtime.txt
```

---

## 🔹 STEP 3: Transfer Files to New Server

From **OLD server**:

```bash
scp tgbot_project.tar.gz tgbot_backup.sql user@NEW_SERVER_IP:/home/user/
```

---

## 🔹 STEP 4: Prepare New Server

SSH into the **NEW server**:

```bash
ssh user@NEW_SERVER_IP
```

Install Docker:

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
```

(Optional) Allow non-root Docker usage:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

## 🔹 STEP 5: Extract Project Files

```bash
mkdir ~/tgbot
cd ~/tgbot
tar -xzvf ../tgbot_project.tar.gz
```

---

## 🔹 STEP 6: Start Database Container (Only)

```bash
docker compose up -d db
```

Wait a few seconds, then verify:

```bash
docker compose ps
```

Ensure `tgbot-db` is **running**.

---

## 🔹 STEP 7: Restore Database (New Server)

```bash
docker exec -i tgbot-db psql -U tgbot tgbot < ~/tgbot_backup.sql
```

Verify restore:

```bash
docker compose exec db psql -U tgbot -c "\dt"
```

✔ Tables should be listed

---

## 🔹 STEP 8: Build & Start the Bot

```bash
docker compose up -d --build bot
```

Check logs:

```bash
docker compose logs -f bot
```

Look for:

```
INFO - Using long polling
```

---

## 🔹 STEP 9: Validate Functionality

In Telegram:

- Send `/start`
- Send `/dbbackup`
- Check logs for errors

---

## 🧹 STEP 10: Cleanup (Optional)

After confirming success:

```bash
rm ~/tgbot_backup.sql
rm ~/tgbot_project.tar.gz
```

---

## ⚠️ IMPORTANT DOs & DON'Ts

### ✅ DO
- Always use `pg_dump` for migrations
- Keep backups before upgrades
- Rebuild images after code changes

### ❌ DON'T
- rsync `/var/lib/docker`
- Copy Docker volumes directly
- Mix VPS PostgreSQL with Docker PostgreSQL

---

## 🔄 Monthly Migration / Backup Strategy (Recommended)

- `/dbbackup` daily (Telegram)
- Monthly:
  ```bash
  pg_dump + scp
  ```

---

## 🏁 Final Notes

- This migration method is **safe**, **repeatable**, and **production-grade**
- Works for upgrades, VPS changes, and disaster recovery
- Avoids Docker corruption issues entirely

---

**END OF MIGRATION GUIDE**
