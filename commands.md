DOCKER & DATABASE COMMANDS – TELEGRAM BOT
========================================

PROJECT DIRECTORY
-----------------
All commands should be run from:
~/tgbot


==============================
DOCKER – BASIC CONTROL
==============================

Start bot and database:
docker compose up -d

Stop only the bot:
docker compose stop bot

Stop everything (bot + database):
docker compose down

Restart only the bot:
docker compose restart bot

Restart everything:
docker compose restart

Apply code changes / add modules (REBUILD REQUIRED):
docker compose up -d --build bot


==============================
DOCKER – STATUS & LOGS
==============================

Check running containers:
docker compose ps

Live bot logs:
docker compose logs -f bot

Last 100 bot log lines:
docker compose logs --tail=100 bot

Database logs:
docker compose logs db


==============================
DOCKER – CONTAINER ACCESS
==============================

Enter bot container shell:
docker compose exec bot bash

Enter database container shell:
docker compose exec db bash

Exit container shell:
exit


==============================
DATABASE – MANUAL ACCESS
==============================

Open PostgreSQL prompt:
docker compose exec db psql -U tgbot tgbot

List all databases:
docker compose exec db psql -U tgbot -l

List all users:
docker compose exec db psql -U postgres -c "\du"


==============================
DATABASE – BACKUP & RESTORE
==============================

Manual database backup (host):
docker exec tgbot-db pg_dump -U tgbot tgbot > backup.sql

Restore database from backup:
docker exec -i tgbot-db psql -U tgbot tgbot < backup.sql

Verify backup file:
ls -lh backup.sql


==============================
DATABASE – CREATE / FIX
==============================

Create database:
docker exec tgbot-db createdb -U tgbot tgbot

Create user manually:
docker exec -it tgbot-db psql -U postgres
CREATE USER tgbot WITH PASSWORD 'mypass';
CREATE DATABASE tgbot OWNER tgbot;
\q


==============================
DOCKER – DEBUGGING
==============================

Check Docker daemon status (host):
sudo systemctl status docker

Start Docker daemon:
sudo systemctl start docker

Enable Docker on boot:
sudo systemctl enable docker

List all containers:
docker ps

List all images:
docker images

Check Docker disk usage:
docker system df


==============================
DOCKER – SAFE CLEANUP
==============================

Remove unused images:
docker image prune -f

Remove stopped containers:
docker container prune -f

⚠️ DO NOT RUN (WILL DELETE DATABASE):
docker volume prune


==============================
EMERGENCY / QUICK FIX
==============================

Bot not responding:
docker compose restart bot

Bot crashed after code change:
docker compose up -d --build bot

Server rebooted:
docker compose up -d

Manual DB backup from Telegram:
Use /dbbackup command


==============================
IMPORTANT NOTES
==============================

- Always rebuild the bot after code changes
- Restart alone does NOT load new modules
- Docker volumes store database data safely
- Never rsync /var/lib/docker
- Always use pg_dump for migrations
- Logs are your first debugging tool

END OF FILE
