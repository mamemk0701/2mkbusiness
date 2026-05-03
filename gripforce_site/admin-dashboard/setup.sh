#!/bin/bash
# GripForce Admin Dashboard - Setup Script
# À exécuter sur la VM Ubuntu

set -e

APP_DIR="/home/mame_m_kane/gripforce_admin"
DOMAIN="admin.grip.2mkbusiness.org"
PG_USER="gripforce_admin"
PG_DB="gripforce_db"
PG_PASS="ChangeMe2026"

echo "=== GripForce Admin Setup ==="

# 1. Install PostgreSQL
echo "[1/6] Installation PostgreSQL..."
sudo apt update -y
sudo apt install -y postgresql postgresql-contrib python3-pip python3-venv nginx

# 2. Setup PostgreSQL
echo "[2/6] Configuration PostgreSQL..."
sudo -u postgres psql -c "CREATE USER ${PG_USER} WITH PASSWORD '${PG_PASS}';" 2>/dev/null || true
sudo -u postgres psql -c "CREATE DATABASE ${PG_DB} OWNER ${PG_USER};" 2>/dev/null || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${PG_DB} TO ${PG_USER};" 2>/dev/null || true

# 3. Setup Python venv
echo "[3/6] Setup Python..."
mkdir -p ${APP_DIR}
cp -r backend/* ${APP_DIR}/
cd ${APP_DIR}
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Systemd service
echo "[4/6] Service systemd..."
sudo cp gripforce-admin.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gripforce-admin
sudo systemctl restart gripforce-admin

# 5. Nginx
echo "[5/6] Configuration Nginx..."
sudo cp nginx-admin.conf /etc/nginx/sites-available/${DOMAIN}
sudo ln -sf /etc/nginx/sites-available/${DOMAIN} /etc/nginx/sites-enabled/
sudo cp -r frontend/* /var/www/${DOMAIN}/
sudo nginx -t && sudo systemctl reload nginx

# 6. SSL (si certbot dispo)
echo "[6/6] SSL..."
if command -v certbot &>/dev/null; then
  sudo certbot --nginx -d ${DOMAIN} --non-interactive --agree-tos -m mame@2mkbusiness.org
fi

echo "=== Setup terminé ! ==="
echo "Accès admin : https://${DOMAIN}"
echo "Users : trex / mmk"
