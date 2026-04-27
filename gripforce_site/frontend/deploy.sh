#!/usr/bin/env bash
# ==========================================
# GripForce - Script de déploiement frontend
# À exécuter depuis /home/mame_m_kane/gripforce_site/frontend/
# ==========================================

set -e  # Stop on error

echo "🎯 GripForce - Déploiement frontend"
echo "===================================="

# Vérifier qu'on est dans le bon dossier
if [ ! -f "package.json" ]; then
    echo "❌ package.json introuvable. Lance ce script depuis le dossier frontend/"
    exit 1
fi

# Vérifier Node version
NODE_VERSION=$(node --version)
echo "✓ Node version: $NODE_VERSION"

# Installer les dépendances
echo ""
echo "📦 Installation des dépendances..."
npm install --no-audit --no-fund

# Build
echo ""
echo "🔨 Build de production..."
npm run build

# Vérifier que dist/ existe
if [ ! -d "dist" ]; then
    echo "❌ Build échoué - dossier dist/ introuvable"
    exit 1
fi

# Afficher le résumé
echo ""
echo "✅ Build terminé avec succès !"
echo ""
echo "📊 Contenu de dist/ :"
ls -lh dist/ | head -10
echo ""
echo "🌐 Le site est prêt dans : $(pwd)/dist"
echo "📍 Nginx sert déjà ce dossier via le vhost gripforce-2mkbusiness"
echo ""
echo "🚀 Pour tester : curl -I https://grip.2mkbusiness.org"
