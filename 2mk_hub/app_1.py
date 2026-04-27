from flask import Flask, render_template_string
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

SITE_HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2MK Business · Innovation & Commerce au Sénégal</title>
    <meta name="description" content="2MK Business - Entreprise sénégalaise spécialisée dans les produits innovants. Découvrez Guindima (trackers GPS) et GripForce (exerciseur de main).">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
    <style>
        :root {
            --dark: #0a0e17;
            --dark-2: #111827;
            --dark-3: #1c2333;
            --gold: #d4a853;
            --gold-dim: rgba(212,168,83,0.12);
            --gold-glow: rgba(212,168,83,0.25);
            --white: #ffffff;
            --gray-100: #f3f4f6;
            --gray-300: #9ca3af;
            --gray-500: #6b7280;
            --radius: 20px;
            --radius-sm: 12px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body { font-family: 'Sora', sans-serif; background: var(--dark); color: var(--white); line-height: 1.6; overflow-x: hidden; }

        /* Grain overlay */
        body::before {
            content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
            pointer-events: none; z-index: 0;
        }

        /* ===== NAV ===== */
        .nav {
            position: fixed; top: 0; width: 100%; z-index: 100;
            padding: 16px 40px; display: flex; justify-content: space-between; align-items: center;
            background: rgba(10,14,23,0.85); backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(255,255,255,0.04);
        }
        .nav-brand { display: flex; align-items: center; gap: 14px; text-decoration: none; color: var(--white); }
        .nav-brand-icon {
            width: 38px; height: 38px; border-radius: 10px;
            background: linear-gradient(135deg, var(--gold), #b8922e);
            display: flex; align-items: center; justify-content: center;
            font-weight: 800; font-size: 14px; color: var(--dark);
        }
        .nav-brand-text { font-weight: 700; font-size: 17px; }
        .nav-links { display: flex; gap: 32px; align-items: center; }
        .nav-links a { color: var(--gray-300); text-decoration: none; font-size: 14px; font-weight: 500; transition: color 0.2s; }
        .nav-links a:hover { color: var(--white); }
        .nav-cta { background: var(--gold); color: var(--dark); padding: 10px 24px; border-radius: 50px; font-weight: 700; font-size: 13px; transition: all 0.25s; }
        .nav-cta:hover { transform: translateY(-1px); box-shadow: 0 6px 20px var(--gold-glow); }
        .menu-btn { display: none; background: none; border: none; cursor: pointer; }
        .menu-btn span { display: block; width: 22px; height: 2px; background: white; margin: 5px 0; border-radius: 2px; }
        .mobile-nav { display: none; position: fixed; top: 70px; left: 0; right: 0; background: var(--dark-2); padding: 24px; z-index: 99; flex-direction: column; gap: 16px; border-bottom: 1px solid rgba(255,255,255,0.06); }
        .mobile-nav.open { display: flex; }
        .mobile-nav a { color: var(--gray-300); text-decoration: none; font-size: 16px; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
        @media (max-width: 768px) {
            .nav { padding: 14px 20px; }
            .nav-links { display: none; }
            .menu-btn { display: block; }
        }

        /* ===== HERO ===== */
        .hero {
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
            text-align: center; padding: 140px 24px 100px; position: relative;
        }
        .hero::before {
            content: ''; position: absolute; top: 10%; left: 50%; transform: translateX(-50%);
            width: 700px; height: 700px; border-radius: 50%;
            background: radial-gradient(circle, var(--gold-dim) 0%, transparent 70%);
            pointer-events: none;
        }
        .hero-content { position: relative; z-index: 1; max-width: 800px; }
        .hero-tag {
            display: inline-flex; align-items: center; gap: 8px;
            background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
            padding: 8px 20px; border-radius: 50px; font-size: 13px; color: var(--gray-300);
            margin-bottom: 32px;
        }
        .hero-tag .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--gold); }
        .hero h1 { font-family: 'Instrument Serif', serif; font-size: 72px; font-weight: 400; line-height: 1.05; margin-bottom: 24px; }
        .hero h1 em { font-style: italic; color: var(--gold); }
        .hero p { font-size: 18px; color: var(--gray-300); max-width: 560px; margin: 0 auto 44px; line-height: 1.7; }
        .hero-buttons { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
        .btn-hero { display: inline-flex; align-items: center; gap: 10px; padding: 16px 32px; border-radius: 50px; font-weight: 700; font-size: 15px; text-decoration: none; transition: all 0.3s; }
        .btn-gold { background: var(--gold); color: var(--dark); }
        .btn-gold:hover { transform: translateY(-2px); box-shadow: 0 8px 30px var(--gold-glow); }
        .btn-outline { background: transparent; color: var(--white); border: 1px solid rgba(255,255,255,0.15); }
        .btn-outline:hover { background: rgba(255,255,255,0.05); border-color: rgba(255,255,255,0.25); }
        .hero-stats { display: flex; justify-content: center; gap: 60px; margin-top: 72px; padding-top: 40px; border-top: 1px solid rgba(255,255,255,0.06); }
        .hero-stat-value { font-size: 36px; font-weight: 800; color: var(--gold); }
        .hero-stat-label { font-size: 13px; color: var(--gray-500); margin-top: 4px; }
        @media (max-width: 768px) {
            .hero { padding: 120px 20px 80px; }
            .hero h1 { font-size: 42px; }
            .hero p { font-size: 16px; }
            .hero-stats { gap: 32px; flex-wrap: wrap; }
        }

        /* ===== SECTION ===== */
        .section { padding: 100px 24px; position: relative; z-index: 1; }
        .section-inner { max-width: 1100px; margin: 0 auto; }
        .section-tag { display: inline-flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 700; color: var(--gold); text-transform: uppercase; letter-spacing: 3px; margin-bottom: 16px; }
        .section-title { font-family: 'Instrument Serif', serif; font-size: 48px; font-weight: 400; line-height: 1.15; margin-bottom: 20px; }
        .section-subtitle { font-size: 17px; color: var(--gray-300); max-width: 560px; line-height: 1.7; }
        @media (max-width: 768px) { .section-title { font-size: 36px; } }

        /* ===== BRANDS ===== */
        .brands-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; margin-top: 56px; }
        .brand-card {
            background: var(--dark-2); border: 1px solid rgba(255,255,255,0.06);
            border-radius: var(--radius); overflow: hidden; transition: all 0.4s;
            text-decoration: none; color: var(--white); display: flex; flex-direction: column;
        }
        .brand-card:hover { border-color: rgba(255,255,255,0.12); transform: translateY(-4px); box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
        .brand-card-visual { height: 280px; display: flex; align-items: center; justify-content: center; overflow: hidden; }
        .brand-card-visual img { max-height: 180px; object-fit: contain; filter: drop-shadow(0 10px 30px rgba(0,0,0,0.4)); transition: transform 0.4s; }
        .brand-card:hover .brand-card-visual img { transform: scale(1.08); }
        .brand-guindima .brand-card-visual { background: linear-gradient(145deg, #1a2744, #2d3a54); }
        .brand-gripforce .brand-card-visual { background: linear-gradient(145deg, #111111, #1a1a2e); }
        .brand-card-content { padding: 32px; flex: 1; display: flex; flex-direction: column; }
        .brand-card-badge { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 14px; color: var(--gold); }
        .brand-card-badge .badge-dot { width: 5px; height: 5px; border-radius: 50%; }
        .brand-card h3 { font-family: 'Instrument Serif', serif; font-size: 28px; font-weight: 400; margin-bottom: 10px; }
        .brand-card p { font-size: 14px; color: var(--gray-300); line-height: 1.7; margin-bottom: 24px; flex: 1; }
        .brand-card-meta { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 24px; }
        .brand-meta-item { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--gray-500); }
        .brand-meta-item .meta-dot { width: 4px; height: 4px; border-radius: 50%; background: var(--gold); }
        .brand-card-link { display: inline-flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 700; color: var(--gold); text-decoration: none; transition: gap 0.3s; }
        .brand-card:hover .brand-card-link { gap: 14px; }
        .brand-card-link svg { width: 16px; height: 16px; transition: transform 0.3s; }
        .brand-card:hover .brand-card-link svg { transform: translateX(4px); }
        @media (max-width: 768px) { .brands-grid { grid-template-columns: 1fr; } .brand-card-visual { height: 200px; } }

        /* ===== ABOUT ===== */
        .about-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; margin-top: 56px; }
        .about-text p { font-size: 16px; color: var(--gray-300); line-height: 1.8; margin-bottom: 20px; }
        .about-values { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 36px; }
        .value-card { background: var(--dark-2); border: 1px solid rgba(255,255,255,0.06); border-radius: var(--radius-sm); padding: 24px; transition: border-color 0.3s; }
        .value-card:hover { border-color: var(--gold); }
        .value-icon { font-size: 28px; margin-bottom: 12px; }
        .value-card h4 { font-size: 15px; font-weight: 700; margin-bottom: 6px; }
        .value-card p { font-size: 13px; color: var(--gray-500); line-height: 1.6; }
        .about-visual { display: flex; flex-direction: column; gap: 20px; }
        .about-number-card { background: var(--dark-2); border: 1px solid rgba(255,255,255,0.06); border-radius: var(--radius-sm); padding: 28px; text-align: center; }
        .about-number { font-size: 48px; font-weight: 800; color: var(--gold); }
        .about-number-label { font-size: 13px; color: var(--gray-500); margin-top: 4px; }
        @media (max-width: 768px) { .about-grid { grid-template-columns: 1fr; gap: 40px; } .about-values { grid-template-columns: 1fr; } }

        /* ===== CTA ===== */
        .cta { text-align: center; padding: 100px 24px; background: linear-gradient(180deg, var(--dark) 0%, var(--dark-2) 100%); position: relative; }
        .cta::before { content: ''; position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 500px; height: 500px; border-radius: 50%; background: radial-gradient(circle, var(--gold-dim) 0%, transparent 70%); }
        .cta-content { position: relative; z-index: 1; }
        .cta h2 { font-family: 'Instrument Serif', serif; font-size: 44px; margin-bottom: 16px; }
        .cta p { color: var(--gray-300); font-size: 17px; margin-bottom: 40px; max-width: 480px; margin-left: auto; margin-right: auto; }
        .cta-btn { display: inline-flex; align-items: center; gap: 10px; background: var(--gold); color: var(--dark); padding: 18px 40px; border-radius: 50px; font-weight: 700; font-size: 16px; text-decoration: none; transition: all 0.3s; }
        .cta-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 40px var(--gold-glow); }
        .cta-btn svg { width: 20px; height: 20px; fill: currentColor; }

        /* ===== FOOTER ===== */
        .footer { border-top: 1px solid rgba(255,255,255,0.04); padding: 48px 24px 32px; position: relative; z-index: 1; }
        .footer-inner { max-width: 1100px; margin: 0 auto; }
        .footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 40px; margin-bottom: 40px; }
        .footer-brand h3 { font-size: 18px; font-weight: 700; margin-bottom: 10px; }
        .footer-brand p { font-size: 13px; color: var(--gray-500); line-height: 1.7; }
        .footer-col h4 { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; color: var(--gray-500); margin-bottom: 16px; }
        .footer-col a { display: block; color: var(--gray-300); text-decoration: none; font-size: 14px; margin-bottom: 10px; transition: color 0.2s; }
        .footer-col a:hover { color: var(--gold); }
        .footer-social { display: flex; gap: 10px; margin-top: 16px; }
        .footer-social a { width: 38px; height: 38px; border-radius: 50%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; justify-content: center; transition: all 0.25s; }
        .footer-social a:hover { background: var(--gold); border-color: var(--gold); }
        .footer-social a svg { width: 16px; height: 16px; fill: white; }
        .footer-bottom { border-top: 1px solid rgba(255,255,255,0.04); padding-top: 24px; text-align: center; font-size: 12px; color: var(--gray-500); }
        @media (max-width: 768px) { .footer-grid { grid-template-columns: 1fr; } }

        /* Animations */
        .fade-in { opacity: 0; transform: translateY(30px); transition: all 0.7s ease; }
        .fade-in.visible { opacity: 1; transform: translateY(0); }
    </style>
</head>
<body>

    <!-- NAV -->
    <nav class="nav">
        <a href="#" class="nav-brand">
            <div class="nav-brand-icon">2MK</div>
            <span class="nav-brand-text">2MK Business</span>
        </a>
        <div class="nav-links">
            <a href="#marques">Nos marques</a>
            <a href="#apropos">À propos</a>
            <a href="#contact">Contact</a>
            <a href="https://wa.me/221767593281?text=Bonjour%2C%20je%20m%27int%C3%A9resse%20%C3%A0%202MK%20Business" class="nav-cta">Nous contacter</a>
        </div>
        <button class="menu-btn" onclick="document.getElementById('mobileNav').classList.toggle('open')">
            <span></span><span></span><span></span>
        </button>
    </nav>
    <div class="mobile-nav" id="mobileNav">
        <a href="#marques" onclick="this.parentElement.classList.remove('open')">Nos marques</a>
        <a href="#apropos" onclick="this.parentElement.classList.remove('open')">À propos</a>
        <a href="#contact" onclick="this.parentElement.classList.remove('open')">Contact</a>
        <a href="https://wa.me/221767593281" style="color:var(--gold);font-weight:700;">Nous contacter</a>
    </div>

    <!-- HERO -->
    <section class="hero">
        <div class="hero-content">
            <div class="hero-tag"><span class="dot"></span> Dakar, Sénégal · Depuis 2026</div>
            <h1>Des produits <em>innovants</em> pour le quotidien africain</h1>
            <p>2MK Business conçoit et distribue des produits technologiques et lifestyle qui résolvent de vrais problèmes. Made in Senegal, pensés pour vous.</p>
            <div class="hero-buttons">
                <a href="#marques" class="btn-hero btn-gold">Découvrir nos marques ↓</a>
                <a href="https://wa.me/221767593281?text=Bonjour%2C%20je%20m%27int%C3%A9resse%20%C3%A0%202MK%20Business" class="btn-hero btn-outline">Nous contacter</a>
            </div>
            <div class="hero-stats">
                <div><div class="hero-stat-value">2</div><div class="hero-stat-label">Marques lancées</div></div>
                <div><div class="hero-stat-value">24h</div><div class="hero-stat-label">Livraison Dakar</div></div>
                <div><div class="hero-stat-value">100%</div><div class="hero-stat-label">Made in Senegal</div></div>
            </div>
        </div>
    </section>

    <!-- BRANDS -->
    <section class="section" id="marques">
        <div class="section-inner">
            <div class="section-tag">● Nos marques</div>
            <h2 class="section-title fade-in">Chaque marque,<br>une mission.</h2>
            <p class="section-subtitle fade-in">Des produits pensés pour résoudre des problèmes concrets du quotidien sénégalais et africain.</p>

            <div class="brands-grid">
                <!-- GUINDIMA -->
                <a href="https://guindima.2mkbusiness.org" class="brand-card brand-guindima fade-in" target="_blank">
                    <div class="brand-card-visual">
                        <img src="https://guindima.2mkbusiness.org/static/images/tracker_blanc.png" alt="Guindima Tracker GPS" onerror="this.style.display='none'">
                    </div>
                    <div class="brand-card-content">
                        <div class="brand-card-badge"><span class="badge-dot" style="background:#3b82f6;"></span> Technologie · GPS</div>
                        <h3>Guindima</h3>
                        <p>Tracker GPS compact pour localiser vos proches en temps réel. Enfants, parents âgés, véhicules, objets de valeur. Compatible iOS & Android, autonomie 1-2 ans.</p>
                        <div class="brand-card-meta">
                            <span class="brand-meta-item"><span class="meta-dot"></span> À partir de 9 000 F</span>
                            <span class="brand-meta-item"><span class="meta-dot"></span> 5 produits</span>
                            <span class="brand-meta-item"><span class="meta-dot"></span> iOS & Android</span>
                        </div>
                        <span class="brand-card-link">Voir le site Guindima <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
                    </div>
                </a>

                <!-- GRIPFORCE -->
                <a href="https://grip.2mkbusiness.org" class="brand-card brand-gripforce fade-in" target="_blank">
                    <div class="brand-card-visual">
                        <img src="https://grip.2mkbusiness.org/images/grip-1.webp" alt="GripForce" onerror="this.style.display='none'">
                    </div>
                    <div class="brand-card-content">
                        <div class="brand-card-badge"><span class="badge-dot" style="background:#10b981;"></span> Fitness · Santé</div>
                        <h3>GripForce</h3>
                        <p>Exerciseur de main compact en silicone médical. Renforce doigts, poignets et avant-bras en 5 minutes par jour. Picots massants anti-stress inclus.</p>
                        <div class="brand-card-meta">
                            <span class="brand-meta-item"><span class="meta-dot"></span> 4 500 F</span>
                            <span class="brand-meta-item"><span class="meta-dot"></span> Silicone médical</span>
                            <span class="brand-meta-item"><span class="meta-dot"></span> 6 points de préhension</span>
                        </div>
                        <span class="brand-card-link">Voir le site GripForce <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
                    </div>
                </a>
            </div>
        </div>
    </section>

    <!-- ABOUT -->
    <section class="section" id="apropos" style="background: var(--dark-2);">
        <div class="section-inner">
            <div class="about-grid">
                <div class="about-text fade-in">
                    <div class="section-tag">● À propos</div>
                    <h2 class="section-title">Créer ce qui manque au marché.</h2>
                    <p>2MK Business est une entreprise sénégalaise fondée à Dakar avec une vision simple : concevoir et distribuer des produits innovants qui répondent à de vrais besoins du quotidien.</p>
                    <p>Chaque produit est sélectionné, testé et distribué avec un seul objectif : apporter une solution concrète, accessible et de qualité au marché sénégalais et africain.</p>
                    <div class="about-values">
                        <div class="value-card"><div class="value-icon">🎯</div><h4>Utile d'abord</h4><p>Chaque produit résout un vrai problème. Pas de gadgets, que de l'essentiel.</p></div>
                        <div class="value-card"><div class="value-icon">⚡</div><h4>Rapide</h4><p>Livraison 24h à Dakar. Paiement Wave et Orange Money.</p></div>
                        <div class="value-card"><div class="value-icon">🤝</div><h4>Accessible</h4><p>Des prix justes, adaptés au pouvoir d'achat local.</p></div>
                        <div class="value-card"><div class="value-icon">🇸🇳</div><h4>Local</h4><p>Conçu et distribué depuis Dakar, pour le Sénégal et l'Afrique.</p></div>
                    </div>
                </div>
                <div class="about-visual fade-in">
                    <div class="about-number-card"><div class="about-number">2</div><div class="about-number-label">Marques en activité</div></div>
                    <div class="about-number-card"><div class="about-number">24h</div><div class="about-number-label">Livraison Dakar & banlieue</div></div>
                    <div class="about-number-card"><div class="about-number">2026</div><div class="about-number-label">Année de lancement</div></div>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA -->
    <section class="cta" id="contact">
        <div class="cta-content fade-in">
            <h2>Un projet ? Une question ?</h2>
            <p>Contactez-nous sur WhatsApp. On répond vite.</p>
            <a href="https://wa.me/221767593281?text=Bonjour%2C%20je%20m%27int%C3%A9resse%20%C3%A0%202MK%20Business" class="cta-btn">
                <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.612.616l4.532-1.47A11.946 11.946 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.24 0-4.313-.724-5.996-1.95l-.418-.31-2.689.872.892-2.636-.342-.442A9.935 9.935 0 012 12C2 6.486 6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z"/></svg>
                Écrire sur WhatsApp
            </a>
        </div>
    </section>

    <!-- FOOTER -->
    <footer class="footer">
        <div class="footer-inner">
            <div class="footer-grid">
                <div class="footer-brand">
                    <h3>2MK Business</h3>
                    <p>Entreprise sénégalaise spécialisée dans la conception et la distribution de produits innovants pour le quotidien.</p>
                    <div class="footer-social">
                        <a href="https://www.tiktok.com/@2mk_business" target="_blank" title="TikTok"><svg viewBox="0 0 24 24"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1v-3.5a6.37 6.37 0 00-.79-.05A6.34 6.34 0 003.15 15.2a6.34 6.34 0 0010.86 4.46V13a8.2 8.2 0 005.58 2.18V11.7a4.83 4.83 0 01-3.77-1.78V6.69h3.77z"/></svg></a>
                        <a href="https://www.instagram.com/2mk_business" target="_blank" title="Instagram"><svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg></a>
                        <a href="https://wa.me/221767593281" target="_blank" title="WhatsApp"><svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.612.616l4.532-1.47A11.946 11.946 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.24 0-4.313-.724-5.996-1.95l-.418-.31-2.689.872.892-2.636-.342-.442A9.935 9.935 0 012 12C2 6.486 6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z"/></svg></a>
                    </div>
                </div>
                <div class="footer-col">
                    <h4>Marques</h4>
                    <a href="https://guindima.2mkbusiness.org" target="_blank">Guindima</a>
                    <a href="https://grip.2mkbusiness.org" target="_blank">GripForce</a>
                </div>
                <div class="footer-col">
                    <h4>Contact</h4>
                    <a href="https://wa.me/221767593281">WhatsApp</a>
                    <a href="#">Dakar, Sénégal</a>
                    <a href="#">+221 76 759 32 81</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2026 2MK Business. Tous droits réservés. Conçu avec ♥ à Dakar.</p>
            </div>
        </div>
    </footer>

    <script>
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); });
    }, { threshold: 0.1 });
    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
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
