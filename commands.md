# 🐳 Docker & Database Commands  
## Telegram Bot – Operations Handbook

> **Project directory:** `~/tgbot`  
> Run all commands from this directory unless stated otherwise.

---

## 📦 Docker – Basic Control

### ▶️ Start bot and database
```bash
docker compose up -d
```

### 🛑 Stop only the bot
```bash
docker compose stop bot
```

### 🛑 Stop everything (bot + database)
```bash
docker compose down
```

> ℹ️ Database data is preserved (Docker volume is not deleted).

---

## 🔁 Restart

### Restart only the bot
```bash
docker compose restart bot
```

### Restart everything
```bash
docker compose restart
```

---

## 🔨 Apply Code Changes (IMPORTANT)

> Use this **after any code change**, new module, or logic update.

```bash
docker compose up -d --build bot
```

⚠️ Restart alone **will NOT** load new code.

---

## 📊 Status & Logs

### Check container status
```bash
docker compose ps
```

### Live bot logs
```bash
docker compose logs -f bot
```

### Last 100 bot log lines
```bash
docker compose logs --tail=100 bot
```

### Database logs
```bash
docker compose logs db
```

---

## 🧪 Container Access (Debugging)

### Enter bot container
```bash
docker compose exec bot bash
```

### Enter database container
```bash
docker compose exec db bash
```

### Exit container shell
```bash
exit
```

---

## 🗄️ PostgreSQL – Manual Access

### Open PostgreSQL prompt
```bash
docker compose exec db psql -U tgbot tgbot
```

### List all databases
```bash
docker compose exec db psql -U tgbot -l
```

### List all database users
```bash
docker compose exec db psql -U postgres -c "\du"
```

---

## 💾 Database Backup & Restore

### Manual backup (host → file)
```bash
docker exec tgbot-db pg_dump -U tgbot tgbot > backup.sql
```

### Restore from backup
```bash
docker exec -i tgbot-db psql -U tgbot tgbot < backup.sql
```

### Verify backup file
```bash
ls -lh backup.sql
```

---

## 🧱 Database Creation / Fixes

### Create database
```bash
docker exec tgbot-db createdb -U tgbot tgbot
```

### Create user & database manually
```bash
docker exec -it tgbot-db psql -U postgres
```

```sql
CREATE USER tgbot WITH PASSWORD 'mypass';
CREATE DATABASE tgbot OWNER tgbot;
\q
```

---

## 🛠 Docker – Debug & Maintenance

### Check Docker daemon status (host)
```bash
sudo systemctl status docker
```

### Start Docker daemon
```bash
sudo systemctl start docker
```

### Enable Docker on boot
```bash
sudo systemctl enable docker
```

### List running containers
```bash
docker ps
```

### List images
```bash
docker images
```

### Docker disk usage
```bash
docker system df
```

---

## 🧹 Safe Cleanup

### Remove unused images
```bash
docker image prune -f
```

### Remove stopped containers
```bash
docker container prune -f
```

🚫 **DO NOT RUN** (will delete database data):
```bash
docker volume prune
```

---

## 🚑 Emergency / Quick Fixes

### Bot not responding
```bash
docker compose restart bot
```

### Bot broken after update
```bash
docker compose up -d --build bot
```

### Server rebooted
```bash
docker compose up -d
```

### Manual database backup (Telegram)
```
/dbbackup
```

---

## 🧠 Operational Notes

- Always rebuild after code changes
- Logs are the **first place to check**
- Docker volumes safely store DB data
- Never rsync `/var/lib/docker`
- Use `pg_dump` for migrations
- Keep this file handy during outages

---

**END OF DOCUMENT**
