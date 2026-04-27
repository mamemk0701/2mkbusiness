from flask import Flask, render_template_string
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

SITE_HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2MK Business · On ne vend pas des produits. On règle des problèmes.</title>
    <meta name="description" content="2MK Business - Entreprise sénégalaise de produits innovants. Guindima (trackers GPS) et GripForce (exerciseur de main). Livraison 24h Dakar.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700;9..40,800&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
    <style>
        :root {
            --navy: #1a2744; --navy-light: #2d3a54; --gold: #d4a853; --gold-light: #e8c97a;
            --gold-bg: #fdf8ef; --white: #ffffff; --gray-50: #f8f9fa; --gray-100: #f0f2f5;
            --gray-200: #e2e6ea; --gray-400: #8c95a0; --gray-600: #5a6370;
            --green: #25D366; --radius: 20px; --radius-sm: 12px;
            --shadow: 0 4px 24px rgba(26,39,68,0.06); --shadow-lg: 0 16px 48px rgba(26,39,68,0.10);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body { font-family: 'DM Sans', sans-serif; background: var(--white); color: var(--navy); line-height: 1.6; }
        .nav { position: fixed; top: 0; width: 100%; z-index: 100; padding: 14px 40px; display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.92); backdrop-filter: blur(16px); border-bottom: 1px solid rgba(0,0,0,0.04); }
        .nav-brand { display: flex; align-items: center; gap: 12px; text-decoration: none; color: var(--navy); }
        .nav-brand img { height: 36px; border-radius: 6px; }
        .nav-brand-text { font-weight: 800; font-size: 17px; }
        .nav-links { display: flex; gap: 32px; align-items: center; }
        .nav-links a { color: var(--gray-600); text-decoration: none; font-size: 14px; font-weight: 500; transition: color 0.2s; }
        .nav-links a:hover { color: var(--navy); }
        .nav-cta { background: var(--navy); color: var(--white); padding: 10px 24px; border-radius: 50px; font-weight: 700; font-size: 13px; transition: all 0.25s; }
        .nav-cta:hover { background: var(--navy-light); transform: translateY(-1px); box-shadow: 0 4px 16px rgba(26,39,68,0.2); }
        .menu-btn { display: none; background: none; border: none; cursor: pointer; }
        .menu-btn span { display: block; width: 22px; height: 2px; background: var(--navy); margin: 5px 0; border-radius: 2px; }
        .mobile-nav { display: none; position: fixed; top: 66px; left: 0; right: 0; background: white; padding: 24px; z-index: 99; flex-direction: column; gap: 16px; box-shadow: var(--shadow-lg); }
        .mobile-nav.open { display: flex; }
        .mobile-nav a { color: var(--gray-600); text-decoration: none; font-size: 16px; padding: 12px 0; border-bottom: 1px solid var(--gray-100); }
        @media (max-width: 768px) { .nav { padding: 12px 20px; } .nav-links { display: none; } .menu-btn { display: block; } }
        .hero { padding: 140px 24px 100px; text-align: center; background: linear-gradient(180deg, var(--white) 0%, var(--gold-bg) 100%); position: relative; overflow: hidden; }
        .hero::before { content: ''; position: absolute; top: -200px; left: 50%; transform: translateX(-50%); width: 800px; height: 800px; border-radius: 50%; background: radial-gradient(circle, rgba(212,168,83,0.08) 0%, transparent 70%); }
        .hero-content { position: relative; z-index: 1; max-width: 780px; margin: 0 auto; }
        .hero-tag { display: inline-flex; align-items: center; gap: 8px; background: var(--white); border: 1px solid var(--gray-200); padding: 8px 20px; border-radius: 50px; font-size: 13px; color: var(--gray-600); margin-bottom: 28px; box-shadow: var(--shadow); }
        .hero-tag .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--gold); }
        .hero h1 { font-family: 'Playfair Display', serif; font-size: 60px; font-weight: 700; line-height: 1.1; margin-bottom: 22px; }
        .hero h1 em { font-style: italic; color: var(--gold); }
        .hero p { font-size: 18px; color: var(--gray-600); max-width: 540px; margin: 0 auto 40px; line-height: 1.7; }
        .hero-buttons { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }
        .btn { display: inline-flex; align-items: center; gap: 10px; padding: 16px 32px; border-radius: 50px; font-weight: 700; font-size: 15px; text-decoration: none; transition: all 0.3s; border: none; cursor: pointer; }
        .btn-gold { background: var(--gold); color: var(--navy); }
        .btn-gold:hover { background: var(--gold-light); transform: translateY(-2px); box-shadow: 0 8px 24px rgba(212,168,83,0.25); }
        .btn-outline { background: var(--white); color: var(--navy); border: 2px solid var(--gray-200); }
        .btn-outline:hover { border-color: var(--navy); }
        .hero-stats { display: flex; justify-content: center; gap: 56px; margin-top: 64px; padding-top: 36px; border-top: 1px solid var(--gray-200); }
        .hero-stat-value { font-size: 32px; font-weight: 800; color: var(--navy); }
        .hero-stat-label { font-size: 13px; color: var(--gray-400); margin-top: 2px; }
        @media (max-width: 768px) { .hero { padding: 120px 20px 80px; } .hero h1 { font-size: 38px; } .hero-stats { gap: 28px; flex-wrap: wrap; } }
        .tagline-bar { background: var(--navy); padding: 16px 0; overflow: hidden; white-space: nowrap; }
        .tagline-track { display: inline-flex; gap: 60px; animation: tscroll 20s linear infinite; }
        .tagline-item { font-size: 14px; font-weight: 600; color: var(--gold); letter-spacing: 1px; }
        @keyframes tscroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
        .section { padding: 100px 24px; }
        .section-inner { max-width: 1100px; margin: 0 auto; }
        .section-tag { display: inline-block; font-size: 12px; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 3px; margin-bottom: 14px; }
        .section-title { font-family: 'Playfair Display', serif; font-size: 44px; font-weight: 700; line-height: 1.15; margin-bottom: 16px; }
        .section-subtitle { font-size: 17px; color: var(--gray-600); max-width: 520px; line-height: 1.7; }
        @media (max-width: 768px) { .section-title { font-size: 32px; } .section { padding: 72px 20px; } }
        .brands-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; margin-top: 52px; }
        .brand-card { background: var(--white); border: 1px solid var(--gray-200); border-radius: var(--radius); overflow: hidden; transition: all 0.35s; text-decoration: none; color: var(--navy); display: flex; flex-direction: column; }
        .brand-card:hover { transform: translateY(-6px); box-shadow: var(--shadow-lg); border-color: var(--gold); }
        .brand-card-visual { height: 300px; display: flex; align-items: center; justify-content: center; padding: 40px; overflow: hidden; }
        .brand-guindima .brand-card-visual { background: linear-gradient(145deg, #1a2744, #2d3a54); }
        .brand-gripforce .brand-card-visual { background: linear-gradient(145deg, #0f0f0f, #1a1a2e); }
        .brand-card-visual img { max-height: 200px; max-width: 80%; object-fit: contain; filter: drop-shadow(0 12px 30px rgba(0,0,0,0.3)); transition: transform 0.4s; }
        .brand-card:hover .brand-card-visual img { transform: scale(1.06) translateY(-4px); }
        .brand-card-content { padding: 32px; flex: 1; display: flex; flex-direction: column; }
        .brand-badge { display: inline-flex; align-items: center; gap: 8px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: var(--gold); margin-bottom: 12px; }
        .brand-badge .bdot { width: 5px; height: 5px; border-radius: 50%; }
        .brand-card h3 { font-family: 'Playfair Display', serif; font-size: 26px; margin-bottom: 10px; }
        .brand-card p { font-size: 14px; color: var(--gray-600); line-height: 1.7; margin-bottom: 20px; flex: 1; }
        .brand-meta { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 20px; }
        .brand-meta span { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--gray-400); }
        .brand-meta span::before { content: ''; width: 4px; height: 4px; border-radius: 50%; background: var(--gold); }
        .brand-link { display: inline-flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 700; color: var(--gold); transition: gap 0.3s; }
        .brand-card:hover .brand-link { gap: 14px; }
        @media (max-width: 768px) { .brands-grid { grid-template-columns: 1fr; } .brand-card-visual { height: 220px; } }
        .about-section { background: var(--gray-50); }
        .about-grid { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 60px; align-items: start; margin-top: 48px; }
        .about-text p { font-size: 16px; color: var(--gray-600); line-height: 1.8; margin-bottom: 18px; }
        .values-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 32px; }
        .value-card { background: var(--white); border: 1px solid var(--gray-200); border-radius: var(--radius-sm); padding: 22px; transition: all 0.3s; }
        .value-card:hover { border-color: var(--gold); box-shadow: var(--shadow); }
        .value-icon { font-size: 24px; margin-bottom: 10px; }
        .value-card h4 { font-size: 14px; font-weight: 700; margin-bottom: 4px; }
        .value-card p { font-size: 13px; color: var(--gray-400); line-height: 1.5; }
        .about-numbers { display: flex; flex-direction: column; gap: 16px; }
        .number-card { background: var(--white); border: 1px solid var(--gray-200); border-radius: var(--radius-sm); padding: 28px; text-align: center; }
        .number-card:hover { border-color: var(--gold); }
        .number-value { font-family: 'Playfair Display', serif; font-size: 44px; font-weight: 700; color: var(--gold); }
        .number-label { font-size: 13px; color: var(--gray-400); margin-top: 4px; }
        @media (max-width: 768px) { .about-grid { grid-template-columns: 1fr; gap: 36px; } .values-grid { grid-template-columns: 1fr; } }
        .cta { background: linear-gradient(145deg, var(--navy), var(--navy-light)); padding: 100px 24px; text-align: center; position: relative; overflow: hidden; }
        .cta::before { content: ''; position: absolute; top: -100px; left: 50%; transform: translateX(-50%); width: 600px; height: 600px; border-radius: 50%; background: radial-gradient(circle, rgba(212,168,83,0.1) 0%, transparent 70%); }
        .cta-inner { position: relative; z-index: 1; }
        .cta h2 { font-family: 'Playfair Display', serif; font-size: 40px; color: var(--white); margin-bottom: 14px; }
        .cta p { color: rgba(255,255,255,0.65); font-size: 17px; margin-bottom: 36px; }
        .cta-btn { display: inline-flex; align-items: center; gap: 10px; background: var(--green); color: var(--white); padding: 18px 40px; border-radius: 50px; font-weight: 700; font-size: 16px; text-decoration: none; transition: all 0.3s; }
        .cta-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(37,211,102,0.3); }
        .cta-btn svg { width: 20px; height: 20px; fill: white; }
        .footer { background: var(--navy); padding: 56px 24px 28px; color: rgba(255,255,255,0.6); }
        .footer-inner { max-width: 1100px; margin: 0 auto; }
        .footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 40px; margin-bottom: 36px; }
        .footer-brand h3 { color: var(--white); font-size: 18px; margin-bottom: 8px; }
        .footer-brand h3 span { color: var(--gold); }
        .footer-brand p { font-size: 13px; line-height: 1.7; }
        .footer-social { display: flex; gap: 10px; margin-top: 16px; }
        .footer-social a { width: 38px; height: 38px; border-radius: 50%; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; transition: all 0.25s; }
        .footer-social a:hover { background: var(--gold); border-color: var(--gold); }
        .footer-social a svg { width: 16px; height: 16px; fill: white; }
        .footer-col h4 { color: rgba(255,255,255,0.4); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 14px; }
        .footer-col a { display: block; color: rgba(255,255,255,0.6); text-decoration: none; font-size: 14px; margin-bottom: 10px; transition: color 0.2s; }
        .footer-col a:hover { color: var(--gold); }
        .footer-bottom { border-top: 1px solid rgba(255,255,255,0.06); padding-top: 20px; text-align: center; font-size: 12px; }
        @media (max-width: 768px) { .footer-grid { grid-template-columns: 1fr; } }
        .fade-up { opacity: 0; transform: translateY(28px); transition: all 0.65s ease; }
        .fade-up.visible { opacity: 1; transform: translateY(0); }
    </style>
</head>
<body>
    <nav class="nav">
        <a href="#" class="nav-brand">
            <img src="/static/images/Logo_2MK_fond_blanc.png" alt="2MK" onerror="this.style.display='none'">
            <div><div class="nav-brand-text">2MK Business</div></div>
        </a>
        <div class="nav-links">
            <a href="#marques">Nos marques</a>
            <a href="#apropos">À propos</a>
            <a href="#contact">Contact</a>
            <a href="https://wa.me/221767593281?text=Bonjour%2C%20je%20m%27int%C3%A9resse%20%C3%A0%202MK%20Business" class="nav-cta">Nous contacter</a>
        </div>
        <button class="menu-btn" onclick="document.getElementById('mobileNav').classList.toggle('open')"><span></span><span></span><span></span></button>
    </nav>
    <div class="mobile-nav" id="mobileNav">
        <a href="#marques" onclick="this.parentElement.classList.remove('open')">Nos marques</a>
        <a href="#apropos" onclick="this.parentElement.classList.remove('open')">À propos</a>
        <a href="#contact" onclick="this.parentElement.classList.remove('open')">Contact</a>
        <a href="https://wa.me/221767593281" style="color:var(--gold);font-weight:700;">Nous contacter</a>
    </div>
    <section class="hero">
        <div class="hero-content">
            <div class="hero-tag"><span class="dot"></span> Dakar, Sénégal · Depuis 2026</div>
            <h1>On ne vend pas des produits. On <em>règle</em> des problèmes.</h1>
            <p>2MK Business conçoit et distribue des produits innovants pour le quotidien sénégalais et africain. Utiles, accessibles et livrés en 24h.</p>
            <div class="hero-buttons">
                <a href="#marques" class="btn btn-gold">Découvrir nos marques ↓</a>
                <a href="https://wa.me/221767593281?text=Bonjour%2C%20je%20m%27int%C3%A9resse%20%C3%A0%202MK%20Business" class="btn btn-outline">Nous contacter</a>
            </div>
            <div class="hero-stats">
                <div><div class="hero-stat-value">2</div><div class="hero-stat-label">Marques</div></div>
                <div><div class="hero-stat-value">24h</div><div class="hero-stat-label">Livraison Dakar</div></div>
                <div><div class="hero-stat-value">Wave & OM</div><div class="hero-stat-label">Paiement mobile</div></div>
            </div>
        </div>
    </section>
    <div class="tagline-bar"><div class="tagline-track">
        <span class="tagline-item">ON NE VEND PAS DES PRODUITS</span><span class="tagline-item">✦</span><span class="tagline-item">ON RÈGLE DES PROBLÈMES</span><span class="tagline-item">✦</span><span class="tagline-item">MADE IN SENEGAL</span><span class="tagline-item">✦</span><span class="tagline-item">LIVRAISON 24H DAKAR</span><span class="tagline-item">✦</span>
        <span class="tagline-item">ON NE VEND PAS DES PRODUITS</span><span class="tagline-item">✦</span><span class="tagline-item">ON RÈGLE DES PROBLÈMES</span><span class="tagline-item">✦</span><span class="tagline-item">MADE IN SENEGAL</span><span class="tagline-item">✦</span><span class="tagline-item">LIVRAISON 24H DAKAR</span><span class="tagline-item">✦</span>
    </div></div>
    <section class="section" id="marques"><div class="section-inner">
        <div class="section-tag">NOS MARQUES</div>
        <h2 class="section-title fade-up">Chaque marque, une mission.</h2>
        <p class="section-subtitle fade-up">Des produits pensés pour résoudre des problèmes concrets du quotidien.</p>
        <div class="brands-grid">
            <a href="https://guindima.2mkbusiness.org" class="brand-card brand-guindima fade-up" target="_blank">
                <div class="brand-card-visual"><img src="https://guindima.2mkbusiness.org/static/images/tracker_blanc.png" alt="Guindima"></div>
                <div class="brand-card-content">
                    <div class="brand-badge"><span class="bdot" style="background:#3b82f6;"></span> Technologie · GPS</div>
                    <h3>Guindima</h3>
                    <p>Tracker GPS compact pour localiser vos proches en temps réel. Enfants, parents âgés, véhicules, objets de valeur. Compatible iOS & Android, autonomie 1-2 ans.</p>
                    <div class="brand-meta"><span>À partir de 9 000 F</span><span>5 produits</span><span>iOS & Android</span></div>
                    <span class="brand-link">Voir le site Guindima →</span>
                </div>
            </a>
            <a href="https://grip.2mkbusiness.org" class="brand-card brand-gripforce fade-up" target="_blank">
                <div class="brand-card-visual"><img src="https://grip.2mkbusiness.org/images/grip-1.webp" alt="GripForce"></div>
                <div class="brand-card-content">
                    <div class="brand-badge"><span class="bdot" style="background:#10b981;"></span> Fitness · Santé</div>
                    <h3>GripForce</h3>
                    <p>Exerciseur de main compact en silicone médical. Renforce doigts, poignets et avant-bras en 5 minutes par jour. Picots massants anti-stress inclus.</p>
                    <div class="brand-meta"><span>4 500 F</span><span>Silicone médical</span><span>6 points de préhension</span></div>
                    <span class="brand-link">Voir le site GripForce →</span>
                </div>
            </a>
        </div>
    </div></section>
    <section class="section about-section" id="apropos"><div class="section-inner"><div class="about-grid">
        <div class="about-text fade-up">
            <div class="section-tag">À PROPOS</div>
            <h2 class="section-title">Créer ce qui manque au marché.</h2>
            <p>2MK Business est une entreprise sénégalaise fondée à Dakar avec une vision simple : concevoir et distribuer des produits innovants qui répondent à de vrais besoins du quotidien.</p>
            <p>Chaque produit est sélectionné, testé et distribué avec un seul objectif — apporter une solution concrète, accessible et de qualité au marché sénégalais et africain.</p>
            <div class="values-grid">
                <div class="value-card"><div class="value-icon">🎯</div><h4>Utile d'abord</h4><p>Chaque produit résout un vrai problème.</p></div>
                <div class="value-card"><div class="value-icon">⚡</div><h4>Rapide</h4><p>Livraison 24h. Paiement Wave & OM.</p></div>
                <div class="value-card"><div class="value-icon">🤝</div><h4>Accessible</h4><p>Des prix adaptés au pouvoir d'achat.</p></div>
                <div class="value-card"><div class="value-icon">🇸🇳</div><h4>Local</h4><p>Depuis Dakar, pour le Sénégal.</p></div>
            </div>
        </div>
        <div class="about-numbers fade-up">
            <div class="number-card"><div class="number-value">2</div><div class="number-label">Marques en activité</div></div>
            <div class="number-card"><div class="number-value">24h</div><div class="number-label">Livraison Dakar & banlieue</div></div>
            <div class="number-card"><div class="number-value">2026</div><div class="number-label">Année de lancement</div></div>
        </div>
    </div></div></section>
    <section class="cta" id="contact"><div class="cta-inner fade-up">
        <h2>Un projet ? Une question ?</h2>
        <p>Contactez-nous sur WhatsApp. On répond vite.</p>
        <a href="https://wa.me/221767593281?text=Bonjour%2C%20je%20m%27int%C3%A9resse%20%C3%A0%202MK%20Business" class="cta-btn">
            <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.612.616l4.532-1.47A11.946 11.946 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.24 0-4.313-.724-5.996-1.95l-.418-.31-2.689.872.892-2.636-.342-.442A9.935 9.935 0 012 12C2 6.486 6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z"/></svg>
            Écrire sur WhatsApp
        </a>
    </div></section>
    <footer class="footer"><div class="footer-inner">
        <div class="footer-grid">
            <div class="footer-brand">
                <h3><span>2MK</span> Business</h3>
                <p>Entreprise sénégalaise spécialisée dans la conception et la distribution de produits innovants pour le quotidien.</p>
                <div class="footer-social">
                    <a href="https://www.tiktok.com/@2mk_business" target="_blank"><svg viewBox="0 0 24 24"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1v-3.5a6.37 6.37 0 00-.79-.05A6.34 6.34 0 003.15 15.2a6.34 6.34 0 0010.86 4.46V13a8.2 8.2 0 005.58 2.18V11.7a4.83 4.83 0 01-3.77-1.78V6.69h3.77z"/></svg></a>
                    <a href="https://www.instagram.com/2mk_business" target="_blank"><svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg></a>
                    <a href="https://wa.me/221767593281" target="_blank"><svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.612.616l4.532-1.47A11.946 11.946 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.24 0-4.313-.724-5.996-1.95l-.418-.31-2.689.872.892-2.636-.342-.442A9.935 9.935 0 012 12C2 6.486 6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z"/></svg></a>
                </div>
            </div>
            <div class="footer-col"><h4>Marques</h4><a href="https://guindima.2mkbusiness.org" target="_blank">Guindima</a><a href="https://grip.2mkbusiness.org" target="_blank">GripForce</a></div>
            <div class="footer-col"><h4>Contact</h4><a href="https://wa.me/221767593281">WhatsApp</a><a href="#">Dakar, Sénégal</a><a href="#">+221 76 759 32 81</a></div>
        </div>
        <div class="footer-bottom">© 2026 2MK Business. Tous droits réservés. Conçu avec ♥ à Dakar.</div>
    </div></footer>
    <script>
    const obs = new IntersectionObserver((e) => { e.forEach(x => { if (x.isIntersecting) x.target.classList.add('visible'); }); }, { threshold: 0.1 });
    document.querySelectorAll('.fade-up').forEach(el => obs.observe(el));
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(SITE_HTML)

@app.route('/health')
def health():
    return {'status': 'ok', 'service': '2mk-business-hub'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
