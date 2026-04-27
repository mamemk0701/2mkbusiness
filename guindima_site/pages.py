GUIDE_HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guide d'utilisation - Guindima</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; background: #f8f9fa; color: #1a2744; }
        .header { background: linear-gradient(135deg, #1a2744 0%, #2d3a54 100%); padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }
        .header a { color: white; text-decoration: none; font-weight: 600; }
        .header .back { opacity: 0.8; font-size: 14px; }
        .hero { background: linear-gradient(135deg, #1a2744 0%, #2d3a54 100%); padding: 40px 20px; text-align: center; color: white; }
        .hero h1 { font-size: 26px; margin-bottom: 10px; }
        .hero p { opacity: 0.9; font-size: 14px; }
        .content { max-width: 800px; margin: 0 auto; padding: 30px 20px; }
        .nav-tabs { display: flex; gap: 10px; margin-bottom: 25px; overflow-x: auto; padding-bottom: 10px; }
        .nav-tab { padding: 10px 20px; background: white; border-radius: 25px; font-size: 13px; font-weight: 500; cursor: pointer; white-space: nowrap; border: 2px solid #eee; transition: all 0.2s; }
        .nav-tab:hover { border-color: #d4a853; }
        .nav-tab.active { background: #1a2744; color: white; border-color: #1a2744; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .section-card { background: white; border-radius: 15px; padding: 25px; margin-bottom: 20px; box-shadow: 0 3px 15px rgba(0,0,0,0.05); }
        .section-card h2 { color: #1a2744; font-size: 18px; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #f0f0f0; }
        .section-card h3 { color: #1a2744; font-size: 15px; margin: 20px 0 10px; }
        .section-card p, .section-card li { color: #555; font-size: 14px; line-height: 1.7; }
        .section-card ul { padding-left: 20px; margin: 10px 0; }
        .section-card li { margin-bottom: 8px; }
        .step-number { background: linear-gradient(135deg, #d4a853, #e8c47a); color: #1a2744; width: 28px; height: 28px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; margin-right: 10px; }
        .tip { background: #fffbf0; border-left: 4px solid #d4a853; padding: 15px; margin: 15px 0; border-radius: 0 10px 10px 0; }
        .tip p { color: #92400e; font-size: 13px; margin: 0; }
        .warning { background: #fef2f2; border-left: 4px solid #ef4444; padding: 15px; margin: 15px 0; border-radius: 0 10px 10px 0; }
        .warning p { color: #991b1b; font-size: 13px; margin: 0; }
        .info { background: #eff6ff; border-left: 4px solid #3b82f6; padding: 15px; margin: 15px 0; border-radius: 0 10px 10px 0; }
        .info p { color: #1e40af; font-size: 13px; margin: 0; }
        .os-badge { display: inline-block; padding: 4px 12px; border-radius: 15px; font-size: 12px; font-weight: 600; margin-right: 8px; }
        .os-badge.ios { background: #000; color: white; }
        .os-badge.android { background: #34a853; color: white; }
        .cta-box { background: linear-gradient(135deg, #1a2744 0%, #2d3a54 100%); border-radius: 15px; padding: 30px; text-align: center; color: white; margin-top: 30px; }
        .cta-box h3 { margin-bottom: 15px; }
        .cta-box a { display: inline-block; background: #25D366; color: white; padding: 12px 30px; border-radius: 25px; text-decoration: none; font-weight: 600; }
        .footer { text-align: center; padding: 30px 20px; color: #666; font-size: 13px; background: #1a2744; }
        .footer p { color: rgba(255,255,255,0.7); margin-bottom: 10px; }
        .social-links { display: flex; justify-content: center; gap: 15px; margin: 15px 0; }
        .social-links a { color: white; font-size: 20px; opacity: 0.8; transition: opacity 0.2s; text-decoration: none; }
        .social-links a:hover { opacity: 1; }
    </style>
</head>
<body>
    <header class="header">
        <a href="/" class="back">← Retour</a>
        <span style="color: #d4a853; font-weight: 600;">GUINDIMA</span>
    </header>
    <section class="hero">
        <h1>📖 Guide d'utilisation</h1>
        <p>Instructions complètes pour votre tracker Guindima</p>
    </section>
    <div class="content">
        <div class="nav-tabs">
            <div class="nav-tab active" onclick="showTab('start')">🚀 Démarrage</div>
            <div class="nav-tab" onclick="showTab('ios')">🍎 iPhone</div>
            <div class="nav-tab" onclick="showTab('android')">🤖 Android</div>
            <div class="nav-tab" onclick="showTab('locate')">📍 Localiser</div>
            <div class="nav-tab" onclick="showTab('advanced')">⚙️ Avancé</div>
            <div class="nav-tab" onclick="showTab('battery')">🔋 Batterie</div>
        </div>
        <div id="start" class="tab-content active">
            <div class="section-card">
                <h2>🚀 Mise en route</h2>
                <h3><span class="step-number">1</span> Allumer le tracker</h3>
                <ul><li>Appuyez une fois sur le bouton du tracker</li><li>Un son de démarrage confirme que le tracker est allumé</li></ul>
                <h3><span class="step-number">2</span> Éteindre le tracker</h3>
                <ul><li>Maintenez le bouton appuyé pendant au moins 3 secondes</li><li>Vous entendrez 2 bips confirmant l'extinction</li></ul>
                <div class="tip"><p>💡 Gardez le tracker allumé en permanence pour pouvoir le localiser à tout moment. La batterie dure 1 à 2 ans !</p></div>
            </div>
            <div class="section-card">
                <h2>📱 Choisissez votre téléphone</h2>
                <p>Le tracker est compatible avec :</p>
                <ul><li><span class="os-badge ios">iOS</span> iPhone avec l'app <strong>Localiser</strong> (Find My)</li><li><span class="os-badge android">Android</span> Téléphones Android avec <strong>Google Find Hub</strong></li></ul>
                <div class="info"><p>ℹ️ Chaque tracker ne peut être associé qu'à <strong>un seul appareil</strong> à la fois.</p></div>
            </div>
        </div>
        <div id="ios" class="tab-content">
            <div class="section-card">
                <h2><span class="os-badge ios">iOS</span> Configuration iPhone</h2>
                <h3><span class="step-number">1</span> Allumez le tracker</h3>
                <p>Appuyez une fois sur le bouton. Attendez le son de démarrage.</p>
                <h3><span class="step-number">2</span> Ouvrez l'app "Localiser"</h3>
                <p>C'est l'app avec l'icône verte "Find My" préinstallée sur votre iPhone.</p>
                <h3><span class="step-number">3</span> Ajoutez le tracker</h3>
                <ul><li>Appuyez sur le <strong>+</strong> en haut</li><li>Sélectionnez <strong>"Ajouter un autre objet"</strong></li><li>Appuyez sur <strong>"Connecter"</strong></li></ul>
                <h3><span class="step-number">4</span> Finalisez la configuration</h3>
                <ul><li>Suivez les instructions à l'écran</li><li>Donnez un nom à votre tracker (ex: "Bracelet Aminata")</li><li>Choisissez un emoji pour l'identifier sur la carte</li></ul>
                <div class="tip"><p>💡 Assurez-vous d'avoir la dernière version d'iOS pour une meilleure compatibilité.</p></div>
            </div>
        </div>
        <div id="android" class="tab-content">
            <div class="section-card">
                <h2><span class="os-badge android">Android</span> Configuration Android</h2>
                <h3>Méthode 1 : Association rapide (Fast Pair)</h3>
                <ul><li><span class="step-number">1</span> Activez le Bluetooth et la connexion réseau</li><li><span class="step-number">2</span> Allumez le tracker (un bip retentit)</li><li><span class="step-number">3</span> Approchez le tracker de votre téléphone</li><li><span class="step-number">4</span> Une notification apparaît automatiquement</li><li><span class="step-number">5</span> Appuyez sur <strong>"Connecter"</strong></li></ul>
                <div class="info"><p>ℹ️ Si aucune notification n'apparaît, redémarrez votre téléphone et réessayez.</p></div>
                <h3 style="margin-top: 25px;">Méthode 2 : Association manuelle</h3>
                <ul><li>Allez dans <strong>Paramètres → Google → Tous les services</strong></li><li>Dans <strong>"Appareils connectés et partage"</strong>, sélectionnez <strong>"Appareils"</strong></li><li>Activez <strong>"Rechercher les appareils à proximité"</strong></li><li>Le tracker apparaîtra dans la liste</li></ul>
            </div>
        </div>
        <div id="locate" class="tab-content">
            <div class="section-card">
                <h2>📍 Localiser votre tracker</h2>
                <h3>🔊 Quand le tracker est à proximité</h3>
                <p><span class="os-badge ios">iOS</span> Dans l'app Localiser :</p>
                <ul><li>Onglet <strong>"Objets"</strong> → Sélectionnez votre tracker</li><li>Appuyez sur <strong>"Émettre un son"</strong></li><li>Suivez le son pour le retrouver</li></ul>
                <p style="margin-top: 15px;"><span class="os-badge android">Android</span> Dans Google Find Hub :</p>
                <ul><li>Sélectionnez votre tracker → <strong>"Faire sonner"</strong></li></ul>
            </div>
            <div class="section-card">
                <h2>🗺️ Voir la position sur la carte</h2>
                <ul><li>La dernière position connue s'affiche sur la carte</li><li>Appuyez sur <strong>"Itinéraire"</strong> pour y aller</li></ul>
                <h3>🔔 Notifications automatiques</h3>
                <ul><li><strong>"Laissé derrière"</strong> : Alerte si vous oubliez le tracker</li><li><strong>"Retrouvé"</strong> : Alerte quand le tracker est localisé par le réseau</li></ul>
            </div>
        </div>
        <div id="advanced" class="tab-content">
            <div class="section-card">
                <h2>🚨 Mode Perdu</h2>
                <p>Si votre tracker est perdu :</p>
                <ul><li>Ouvrez l'app, sélectionnez votre tracker</li><li>Activez <strong>"Mode Perdu"</strong></li><li>Entrez votre numéro/email de contact</li><li>Vous serez notifié quand il sera retrouvé</li></ul>
                <div class="warning"><p>⚠️ En Mode Perdu, le tracker est verrouillé et ne peut pas être associé à un autre appareil.</p></div>
            </div>
            <div class="section-card">
                <h2>🔄 Réinitialiser le tracker</h2>
                <h3>Étape 1 : Dissocier du téléphone</h3>
                <ul><li>Dans l'app, sélectionnez votre tracker</li><li>Appuyez sur <strong>"Supprimer cet objet"</strong></li></ul>
                <h3>Étape 2 : Réinitialisation d'usine</h3>
                <ul><li>Appuyez rapidement 5 fois sur le bouton</li><li>À la 5ème fois, maintenez appuyé jusqu'au bip</li><li>Le tracker est prêt pour un nouvel appareil</li></ul>
            </div>
        </div>
        <div id="battery" class="tab-content">
            <div class="section-card">
                <h2>🔋 Remplacement de la batterie</h2>
                <p>Pile utilisée : <strong>CR2032</strong> (disponible partout)</p>
                <h3><span class="step-number">1</span> Ouvrir le tracker</h3>
                <ul><li>Utilisez l'outil triangulaire fourni</li><li>Insérez-le dans la fente "OPEN" à l'arrière</li></ul>
                <h3><span class="step-number">2</span> Remplacer la pile</h3>
                <ul><li>Retirez l'ancienne pile</li><li>Insérez la nouvelle CR2032 (côté "+" vers le haut)</li></ul>
                <h3><span class="step-number">3</span> Refermer</h3>
                <ul><li>Alignez les encoches et appuyez jusqu'au clic</li></ul>
                <div class="tip"><p>💡 Après remplacement, le tracker reste associé à votre téléphone. Pas besoin de le reconnecter !</p></div>
                <div class="warning"><p>⚠️ Ne jetez pas les piles usagées à la poubelle. Gardez-les hors de portée des enfants.</p></div>
            </div>
        </div>
        <div class="cta-box">
            <h3>Besoin d'aide ?</h3>
            <p style="opacity: 0.9; margin-bottom: 15px;">Notre équipe est disponible pour vous accompagner</p>
            <a href="https://wa.me/221767593281?text=Bonjour%2C%20j'ai%20besoin%20d'aide%20pour%20mon%20tracker%20Guindima">💬 Contacter le support</a>
        </div>
    </div>
    <footer class="footer">
        <p style="color: #d4a853; font-weight: 600;">GUINDIMA</p>
        <p>par 2MK Business</p>
        <div class="social-links">
            <a href="https://www.tiktok.com/@2mk_business" target="_blank" title="TikTok">🎵</a>
            <a href="https://www.instagram.com/2mk_business" target="_blank" title="Instagram">📸</a>
            <a href="https://www.facebook.com/share/18SdwhVNbi/" target="_blank" title="Facebook">📘</a>
            <a href="https://x.com/2mkbusiness" target="_blank" title="X">✖</a>
        </div>
        <p>© 2026 Guindima</p>
    </footer>
    <script>
        function showTab(tabId) { document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active')); document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active')); document.getElementById(tabId).classList.add('active'); event.target.classList.add('active'); }
    </script>
</body>
</html>
'''

CONTENU_HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contenu du kit - Guindima</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; background: #f8f9fa; color: #1a2744; }
        .header { background: linear-gradient(135deg, #1a2744 0%, #2d3a54 100%); padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; }
        .header a { color: white; text-decoration: none; font-weight: 600; }
        .header .back { opacity: 0.8; font-size: 14px; }
        .hero { background: linear-gradient(135deg, #1a2744 0%, #2d3a54 100%); padding: 40px 20px; text-align: center; color: white; }
        .hero h1 { font-size: 26px; margin-bottom: 10px; }
        .hero p { opacity: 0.9; font-size: 14px; }
        .content { max-width: 900px; margin: 0 auto; padding: 30px 20px; }
        .kit-section { background: white; border-radius: 15px; padding: 25px; margin-bottom: 25px; box-shadow: 0 3px 15px rgba(0,0,0,0.05); }
        .kit-section h2 { color: #1a2744; font-size: 20px; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #f0f0f0; }
        .kit-section.featured { border: 2px solid #d4a853; }
        .kit-section.featured h2 { color: #d4a853; }
        .item-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 15px; }
        .item { text-align: center; padding: 20px 10px; background: #f8f9fa; border-radius: 12px; }
        .item-icon { font-size: 32px; margin-bottom: 10px; }
        .item h4 { color: #1a2744; margin-bottom: 5px; font-size: 12px; font-weight: 600; }
        .item p { color: #666; font-size: 11px; line-height: 1.4; }
        .note { background: #eff6ff; border-left: 4px solid #3b82f6; padding: 15px; margin-top: 20px; border-radius: 0 10px 10px 0; }
        .note p { color: #1e40af; font-size: 13px; margin: 0; }
        .accessory-section { margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee; }
        .accessory-section h3 { font-size: 15px; color: #1a2744; margin-bottom: 15px; }
        .accessory-item { display: flex; gap: 15px; margin-bottom: 15px; padding: 15px; background: #f8f9fa; border-radius: 10px; }
        .accessory-item .icon { font-size: 28px; }
        .accessory-item .text h4 { font-size: 14px; color: #1a2744; margin-bottom: 5px; }
        .accessory-item .text p { font-size: 12px; color: #666; line-height: 1.5; }
        .cta-box { background: linear-gradient(135deg, #1a2744 0%, #2d3a54 100%); border-radius: 15px; padding: 30px; text-align: center; color: white; margin-top: 30px; }
        .cta-box h3 { margin-bottom: 15px; }
        .cta-box a { display: inline-block; background: #25D366; color: white; padding: 12px 30px; border-radius: 25px; text-decoration: none; font-weight: 600; }
        .footer { text-align: center; padding: 30px 20px; background: #1a2744; }
        .footer p { color: rgba(255,255,255,0.7); font-size: 13px; margin-bottom: 10px; }
        .social-links { display: flex; justify-content: center; gap: 15px; margin: 15px 0; }
        .social-links a { color: white; font-size: 20px; opacity: 0.8; transition: opacity 0.2s; text-decoration: none; }
        .social-links a:hover { opacity: 1; }
    </style>
</head>
<body>
    <header class="header">
        <a href="/" class="back">← Retour</a>
        <span style="color: #d4a853; font-weight: 600;">GUINDIMA</span>
    </header>
    <section class="hero">
        <h1>📦 Contenu du kit</h1>
        <p>Découvrez ce qui est inclus dans chaque offre</p>
    </section>
    <div class="content">
        <div class="kit-section">
            <h2>🔌 Tracker Seul — 13 000 F</h2>
            <div class="item-grid">
                <div class="item"><div class="item-icon">📍</div><h4>Tracker GPS</h4><p>Noir ou Blanc</p></div>
                <div class="item"><div class="item-icon">🔋</div><h4>Pile CR2032</h4><p>Déjà installée</p></div>
                <div class="item"><div class="item-icon">🔧</div><h4>Outil d'ouverture</h4><p>Pour la batterie</p></div>
                <div class="item"><div class="item-icon">📎</div><h4>Support adhésif</h4><p>Pour coller</p></div>
                <div class="item"><div class="item-icon">🔗</div><h4>Lanière</h4><p>Pour accrocher</p></div>
                <div class="item"><div class="item-icon">📄</div><h4>Notice</h4><p>Guide démarrage</p></div>
            </div>
            <div class="accessory-section">
                <h3>À quoi servent les accessoires ?</h3>
                <div class="accessory-item"><div class="icon">🔧</div><div class="text"><h4>Outil d'ouverture triangulaire</h4><p>Permet d'ouvrir facilement le tracker pour remplacer la pile CR2032 quand elle est épuisée (après 1-2 ans d'utilisation).</p></div></div>
                <div class="accessory-item"><div class="icon">📎</div><div class="text"><h4>Support adhésif</h4><p>Permet de coller le tracker sur une surface plane : intérieur de véhicule, valise, cartable, télécommande... Le tracker se clipse dans le support.</p></div></div>
                <div class="accessory-item"><div class="icon">🔗</div><div class="text"><h4>Lanière / Cordon</h4><p>Permet d'accrocher le tracker à un trousseau de clés, une fermeture de sac, un porte-monnaie, ou tout objet avec un anneau.</p></div></div>
            </div>
            <div class="note"><p>ℹ️ <strong>Idéal pour :</strong> véhicules, motos, bagages, valises, clés, sacs, porte-monnaie, télécommandes, animaux de compagnie.</p></div>
        </div>
        <div class="kit-section featured">
            <h2>🦄 Kit Saytu — 17 000 F ⭐ POPULAIRE</h2>
            <div class="item-grid">
                <div class="item"><div class="item-icon">📍</div><h4>Tracker GPS</h4><p>Noir ou Blanc</p></div>
                <div class="item"><div class="item-icon">⌚</div><h4>Bracelet Silicone</h4><p>15 motifs au choix</p></div>
                <div class="item"><div class="item-icon">🔋</div><h4>Pile CR2032</h4><p>Déjà installée</p></div>
                <div class="item"><div class="item-icon">🔧</div><h4>Outil d'ouverture</h4><p>Pour la batterie</p></div>
                <div class="item"><div class="item-icon">📎</div><h4>Support adhésif</h4><p>Pour coller</p></div>
                <div class="item"><div class="item-icon">🔗</div><h4>Lanière</h4><p>Pour accrocher</p></div>
                <div class="item"><div class="item-icon">📄</div><h4>Notice</h4><p>Guide démarrage</p></div>
            </div>
            <div class="note"><p>ℹ️ <strong>Parfait pour les enfants !</strong> Bracelets colorés avec motifs amusants : licornes, dinosaures, donuts, baleines, arcs-en-ciel...</p></div>
        </div>
        <div class="kit-section">
            <h2>🎨 Kit Guëstu — 18 000 F</h2>
            <div class="item-grid">
                <div class="item"><div class="item-icon">📍</div><h4>Tracker GPS</h4><p>Noir ou Blanc</p></div>
                <div class="item"><div class="item-icon">⌚</div><h4>Bracelet Nylon</h4><p>8 couleurs au choix</p></div>
                <div class="item"><div class="item-icon">🔋</div><h4>Pile CR2032</h4><p>Déjà installée</p></div>
                <div class="item"><div class="item-icon">🔧</div><h4>Outil d'ouverture</h4><p>Pour la batterie</p></div>
                <div class="item"><div class="item-icon">📎</div><h4>Support adhésif</h4><p>Pour coller</p></div>
                <div class="item"><div class="item-icon">🔗</div><h4>Lanière</h4><p>Pour accrocher</p></div>
                <div class="item"><div class="item-icon">📄</div><h4>Notice</h4><p>Guide démarrage</p></div>
            </div>
            <div class="note"><p>ℹ️ <strong>Bracelet nylon premium :</strong> Confortable, ajustable et élégant. Idéal pour enfants plus grands et adultes.</p></div>
        </div>
        <div class="kit-section">
            <h2>🛒 Bracelets seuls (accessoires)</h2>
            <div class="item-grid">
                <div class="item"><div class="item-icon">🦄</div><h4>Bracelet Silicone</h4><p>4 000 F<br>15 motifs</p></div>
                <div class="item"><div class="item-icon">🎨</div><h4>Bracelet Nylon</h4><p>5 000 F<br>8 couleurs</p></div>
            </div>
            <div class="note"><p>ℹ️ Achetez des bracelets supplémentaires pour changer de style ou remplacer un bracelet usé.</p></div>
        </div>
        <div class="cta-box">
            <h3>Prêt à commander ?</h3>
            <p style="opacity: 0.9; margin-bottom: 15px;">Contactez-nous sur WhatsApp</p>
            <a href="https://wa.me/221767593281?text=Bonjour%2C%20je%20veux%20commander%20un%20kit%20Guindima">📱 Commander maintenant</a>
        </div>
    </div>
    <footer class="footer">
        <p style="color: #d4a853; font-weight: 600;">GUINDIMA</p>
        <p>par 2MK Business</p>
        <div class="social-links">
            <a href="https://www.tiktok.com/@2mk_business" target="_blank" title="TikTok">🎵</a>
            <a href="https://www.instagram.com/2mk_business" target="_blank" title="Instagram">📸</a>
            <a href="https://www.facebook.com/share/18SdwhVNbi/" target="_blank" title="Facebook">📘</a>
            <a href="https://x.com/2mkbusiness" target="_blank" title="X">✖</a>
        </div>
        <p>© 2026 Guindima</p>
    </footer>
</body>
</html>
'''
