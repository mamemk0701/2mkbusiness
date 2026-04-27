from flask import Flask, render_template_string, jsonify
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

# ============================================================
# SITE VITRINE V2 - GUINDIMA par 2MK Business
# ============================================================

SITE_HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guindima · Tracker GPS pour localiser vos proches</title>
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <link rel="apple-touch-icon" href="/static/apple-touch-icon.png">
    <meta name="description" content="Guindima - Le tracker GPS compact pour localiser vos proches en temps réel. Bracelets colorés, autonomie 1-2 ans, compatible iOS et Android. Livraison 24h Dakar.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --navy: #1a2744;
            --navy-light: #2d3a54;
            --gold: #d4a853;
            --gold-light: #e8c97a;
            --white: #ffffff;
            --gray-50: #f8f9fa;
            --gray-100: #f0f2f5;
            --gray-200: #e2e6ea;
            --gray-400: #8c95a0;
            --gray-600: #5a6370;
            --gray-800: #2d3340;
            --green-whatsapp: #25D366;
            --radius: 16px;
            --radius-sm: 10px;
            --shadow: 0 4px 24px rgba(26,39,68,0.08);
            --shadow-lg: 0 12px 40px rgba(26,39,68,0.12);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body { font-family: 'DM Sans', sans-serif; background: var(--white); color: var(--navy); line-height: 1.6; }

        /* ===== NAVBAR ===== */
        .navbar {
            position: fixed; top: 0; width: 100%; z-index: 1000;
            background: rgba(26,39,68,0.95); backdrop-filter: blur(12px);
            padding: 12px 24px; display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        .navbar-brand {
            display: flex; align-items: center; gap: 12px;
            text-decoration: none; color: var(--white);
        }
        .navbar-brand img { height: 38px; border-radius: 6px; }
        .navbar-brand-text { display: flex; flex-direction: column; }
        .navbar-brand-name { font-weight: 700; font-size: 18px; color: var(--white); letter-spacing: 0.5px; }
        .navbar-brand-sub { font-size: 11px; color: var(--gold); font-weight: 500; letter-spacing: 0.3px; }
        .navbar-links { display: flex; gap: 28px; align-items: center; }
        .navbar-links a {
            color: rgba(255,255,255,0.75); text-decoration: none; font-size: 14px;
            font-weight: 500; transition: color 0.2s;
        }
        .navbar-links a:hover { color: var(--white); }
        .navbar-cta {
            background: var(--green-whatsapp); color: var(--white); padding: 10px 22px;
            border-radius: 50px; text-decoration: none; font-weight: 600; font-size: 14px;
            transition: transform 0.2s, box-shadow 0.2s; display: flex; align-items: center; gap: 8px;
        }
        .navbar-cta:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(37,211,102,0.3); }
        .navbar-cta svg { width: 18px; height: 18px; fill: white; }

        /* Mobile menu */
        .menu-toggle { display: none; background: none; border: none; cursor: pointer; padding: 4px; }
        .menu-toggle span { display: block; width: 22px; height: 2px; background: white; margin: 5px 0; border-radius: 2px; transition: 0.3s; }
        .mobile-menu { display: none; }

        @media (max-width: 768px) {
            .navbar-links { display: none; }
            .menu-toggle { display: block; }
            .mobile-menu {
                position: fixed; top: 56px; left: 0; right: 0;
                background: var(--navy); padding: 20px; z-index: 999;
                display: none; flex-direction: column; gap: 16px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .mobile-menu.active { display: flex; }
            .mobile-menu a {
                color: rgba(255,255,255,0.85); text-decoration: none; font-size: 16px;
                padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.06);
            }
        }

        /* ===== HERO ===== */
        .hero {
            background: linear-gradient(145deg, var(--navy) 0%, var(--navy-light) 100%);
            padding: 120px 24px 80px; position: relative; overflow: hidden;
        }
        .hero::before {
            content: ''; position: absolute; top: -50%; right: -20%; width: 600px; height: 600px;
            background: radial-gradient(circle, rgba(212,168,83,0.08) 0%, transparent 70%);
            border-radius: 50%;
        }
        .hero-inner {
            max-width: 1100px; margin: 0 auto; display: grid;
            grid-template-columns: 1fr 1fr; gap: 60px; align-items: center;
        }
        .hero-content { position: relative; z-index: 1; }
        .hero-badge {
            display: inline-block; background: rgba(212,168,83,0.15); color: var(--gold);
            padding: 6px 16px; border-radius: 50px; font-size: 13px; font-weight: 600;
            margin-bottom: 20px; letter-spacing: 0.5px;
        }
        .hero h1 {
            font-family: 'Playfair Display', serif; font-size: 48px; color: var(--white);
            line-height: 1.15; margin-bottom: 20px;
        }
        .hero h1 em { font-style: normal; color: var(--gold); }
        .hero p { color: rgba(255,255,255,0.8); font-size: 17px; margin-bottom: 32px; max-width: 460px; }
        .hero-buttons { display: flex; gap: 14px; flex-wrap: wrap; }
        .btn {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 14px 28px; border-radius: 50px; font-weight: 600;
            font-size: 15px; text-decoration: none; transition: all 0.25s; cursor: pointer; border: none;
        }
        .btn-primary { background: var(--gold); color: var(--navy); }
        .btn-primary:hover { background: var(--gold-light); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(212,168,83,0.3); }
        .btn-secondary { background: rgba(255,255,255,0.1); color: var(--white); border: 1px solid rgba(255,255,255,0.2); }
        .btn-secondary:hover { background: rgba(255,255,255,0.15); }
        .hero-specs { display: flex; gap: 32px; margin-top: 40px; }
        .hero-spec { text-align: center; }
        .hero-spec-value { color: var(--gold); font-size: 22px; font-weight: 700; }
        .hero-spec-label { color: rgba(255,255,255,0.6); font-size: 12px; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.5px; }
        .hero-image { position: relative; text-align: center; }
        .hero-image img { max-width: 320px; width: 100%; filter: drop-shadow(0 20px 40px rgba(0,0,0,0.3)); animation: float 4s ease-in-out infinite; }
        @keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }

        @media (max-width: 768px) {
            .hero { padding: 100px 20px 60px; }
            .hero-inner { grid-template-columns: 1fr; text-align: center; gap: 40px; }
            .hero h1 { font-size: 32px; }
            .hero p { margin: 0 auto 28px; }
            .hero-buttons { justify-content: center; }
            .hero-specs { justify-content: center; }
            .hero-image img { max-width: 220px; }
        }

        /* ===== MARQUEE ===== */
        .marquee {
            background: var(--gold); padding: 14px 0; overflow: hidden; white-space: nowrap;
        }
        .marquee-track {
            display: inline-flex; gap: 40px; animation: scroll 25s linear infinite;
        }
        .marquee-item { font-size: 14px; font-weight: 600; color: var(--navy); }
        @keyframes scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

        /* ===== SECTIONS ===== */
        .section { padding: 80px 24px; }
        .section-inner { max-width: 1100px; margin: 0 auto; }
        .section-header { text-align: center; margin-bottom: 52px; }
        .section-label {
            display: inline-block; color: var(--gold); font-size: 13px; font-weight: 700;
            text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px;
        }
        .section-title { font-family: 'Playfair Display', serif; font-size: 36px; margin-bottom: 14px; }
        .section-subtitle { color: var(--gray-600); font-size: 16px; max-width: 540px; margin: 0 auto; }

        /* ===== PRODUCTS CARDS ===== */
        .products-grid {
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px;
        }
        @media (max-width: 900px) { .products-grid { grid-template-columns: 1fr; } }
        .product-card {
            background: var(--white); border: 1px solid var(--gray-200); border-radius: var(--radius);
            padding: 28px 22px; text-align: left; transition: all 0.3s; cursor: pointer; position: relative;
        }
        .product-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); border-color: var(--gold); }
        .product-card.popular { border: 2px solid var(--gold); }
        .product-badge {
            position: absolute; top: -1px; right: 20px; background: var(--gold);
            color: var(--navy); font-size: 11px; font-weight: 700; padding: 5px 12px;
            border-radius: 0 0 8px 8px; letter-spacing: 0.5px;
        }
        .product-img { width: 100%; height: 160px; object-fit: contain; margin-bottom: 18px; }
        .product-name { font-size: 18px; font-weight: 700; margin-bottom: 6px; }
        .product-desc { font-size: 13px; color: var(--gray-600); margin-bottom: 14px; line-height: 1.5; }
        .product-price { font-size: 24px; font-weight: 700; color: var(--gold); margin-bottom: 16px; }
        .product-features { list-style: none; margin-bottom: 20px; }
        .product-features li {
            font-size: 13px; color: var(--gray-600); padding: 3px 0;
            display: flex; align-items: center; gap: 8px;
        }
        .product-features li::before { content: '✓'; color: var(--gold); font-weight: 700; }
        .product-btn {
            display: block; width: 100%; padding: 12px; border-radius: 50px;
            font-weight: 600; font-size: 14px; text-align: center; cursor: pointer;
            transition: all 0.2s; border: 2px solid var(--navy); background: var(--white);
            color: var(--navy);
        }
        .product-btn:hover { background: var(--navy); color: var(--white); }
        .product-card.popular .product-btn { background: var(--navy); color: var(--white); }
        .product-card.popular .product-btn:hover { background: var(--navy-light); }

        /* ===== BRACELETS CAROUSEL ===== */
        .bracelets-section { background: var(--gray-50); }
        .bracelet-type { margin-bottom: 48px; }
        .bracelet-type:last-child { margin-bottom: 0; }
        .bracelet-type-header {
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 20px; flex-wrap: wrap; gap: 10px;
        }
        .bracelet-type-title { font-size: 22px; font-weight: 700; }
        .bracelet-type-price { font-size: 18px; font-weight: 700; color: var(--gold); }

        .carousel-wrapper {
            position: relative; overflow: hidden; border-radius: var(--radius);
        }
        .carousel-track {
            display: flex; gap: 16px; animation: carousel-scroll 30s linear infinite;
            width: max-content;
        }
        .carousel-track:hover { animation-play-state: paused; }
        .carousel-item {
            flex: 0 0 140px; background: var(--white); border-radius: var(--radius-sm);
            padding: 12px; text-align: center; cursor: pointer; transition: all 0.2s;
            border: 2px solid transparent;
        }
        .carousel-item:hover { border-color: var(--gold); transform: scale(1.05); }
        .carousel-item img { width: 110px; height: 110px; object-fit: contain; margin-bottom: 8px; border-radius: 8px; }
        .carousel-item p { font-size: 12px; font-weight: 600; color: var(--gray-800); }
        @keyframes carousel-scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

        @media (max-width: 768px) {
            .carousel-item { flex: 0 0 120px; }
            .carousel-item img { width: 90px; height: 90px; }
        }

        /* ===== STEPS ===== */
        .steps-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 32px; counter-reset: step; }
        .step {
            text-align: center; position: relative; counter-increment: step;
        }
        .step::before {
            content: counter(step); display: flex; align-items: center; justify-content: center;
            width: 52px; height: 52px; border-radius: 50%; background: var(--gold);
            color: var(--navy); font-weight: 700; font-size: 20px; margin: 0 auto 18px;
        }
        .step h4 { font-size: 16px; margin-bottom: 8px; }
        .step p { font-size: 13px; color: var(--gray-600); }
        @media (max-width: 768px) { .steps-grid { grid-template-columns: 1fr 1fr; } }
        @media (max-width: 480px) { .steps-grid { grid-template-columns: 1fr; } }

        /* ===== FEATURES ===== */
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 24px; }
        .feature-card {
            background: var(--white); border: 1px solid var(--gray-200); border-radius: var(--radius);
            padding: 28px; transition: all 0.3s;
        }
        .feature-card:hover { box-shadow: var(--shadow); border-color: var(--gold); }
        .feature-icon { font-size: 36px; margin-bottom: 14px; }
        .feature-card h4 { font-size: 17px; margin-bottom: 8px; }
        .feature-card p { font-size: 14px; color: var(--gray-600); }

        /* ===== USAGES ===== */
        .usages-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; }
        .usage-card {
            background: var(--white); border: 1px solid var(--gray-200); border-radius: var(--radius);
            padding: 24px 16px; text-align: center; transition: all 0.3s;
        }
        .usage-card:hover { border-color: var(--gold); transform: translateY(-2px); }
        .usage-icon { font-size: 32px; margin-bottom: 10px; }
        .usage-card p { font-size: 14px; font-weight: 600; }

        /* ===== FAQ ===== */
        .faq-list { max-width: 700px; margin: 0 auto; }
        .faq-item {
            border: 1px solid var(--gray-200); border-radius: var(--radius-sm);
            margin-bottom: 12px; overflow: hidden;
        }
        .faq-question {
            width: 100%; padding: 18px 22px; background: var(--white); border: none;
            text-align: left; font-size: 15px; font-weight: 600; cursor: pointer;
            display: flex; justify-content: space-between; align-items: center;
            font-family: inherit; color: var(--navy);
        }
        .faq-question::after { content: '+'; font-size: 20px; font-weight: 300; transition: transform 0.3s; }
        .faq-question.active::after { transform: rotate(45deg); }
        .faq-answer {
            max-height: 0; overflow: hidden; transition: max-height 0.35s ease;
            padding: 0 22px; font-size: 14px; color: var(--gray-600); line-height: 1.7;
        }
        .faq-answer.active { max-height: 300px; padding: 0 22px 18px; }

        /* ===== CTA ===== */
        .cta-section {
            background: linear-gradient(145deg, var(--navy) 0%, var(--navy-light) 100%);
            padding: 80px 24px; text-align: center;
        }
        .cta-section h2 { font-family: 'Playfair Display', serif; font-size: 32px; color: var(--white); margin-bottom: 16px; }
        .cta-section p { color: rgba(255,255,255,0.7); font-size: 16px; margin-bottom: 32px; }
        .cta-btn {
            display: inline-flex; align-items: center; gap: 10px;
            background: var(--green-whatsapp); color: var(--white);
            padding: 16px 36px; border-radius: 50px; font-weight: 700; font-size: 16px;
            text-decoration: none; transition: all 0.25s;
        }
        .cta-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(37,211,102,0.3); }
        .cta-btn svg { width: 22px; height: 22px; fill: white; }

        /* ===== RESOURCE LINKS ===== */
        .resource-links {
            display: grid; grid-template-columns: 1fr 1fr; gap: 24px;
            max-width: 700px; margin: 40px auto 0;
        }
        .resource-link {
            display: flex; align-items: center; gap: 16px;
            background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
            border-radius: var(--radius); padding: 20px; text-decoration: none;
            transition: all 0.25s;
        }
        .resource-link:hover { background: rgba(255,255,255,0.1); border-color: var(--gold); transform: translateY(-2px); }
        .resource-link-icon { font-size: 28px; }
        .resource-link-text h4 { color: var(--white); font-size: 15px; margin-bottom: 2px; }
        .resource-link-text p { color: rgba(255,255,255,0.6); font-size: 12px; }
        @media (max-width: 600px) { .resource-links { grid-template-columns: 1fr; } }

        /* ===== FOOTER ===== */
        .footer { background: var(--navy); padding: 60px 24px 30px; color: rgba(255,255,255,0.7); }
        .footer-inner { max-width: 1100px; margin: 0 auto; }
        .footer-grid { display: grid; grid-template-columns: 1.5fr 1fr 1fr 1fr; gap: 40px; margin-bottom: 40px; }
        .footer-brand h3 { color: var(--white); font-size: 20px; margin-bottom: 12px; }
        .footer-brand h3 span { color: var(--gold); }
        .footer-brand p { font-size: 14px; line-height: 1.6; }
        .footer-col h4 { color: var(--white); font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px; }
        .footer-col a { display: block; color: rgba(255,255,255,0.6); text-decoration: none; font-size: 14px; margin-bottom: 10px; transition: color 0.2s; }
        .footer-col a:hover { color: var(--gold); }
        .footer-contact-item { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; font-size: 14px; }

        /* Social icons in footer */
        .footer-social { display: flex; gap: 12px; margin-top: 20px; }
        .footer-social a {
            display: flex; align-items: center; justify-content: center;
            width: 42px; height: 42px; border-radius: 50%;
            background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
            transition: all 0.25s;
        }
        .footer-social a:hover { background: var(--gold); border-color: var(--gold); transform: translateY(-2px); }
        .footer-social a svg { width: 20px; height: 20px; fill: white; }

        .footer-bottom {
            border-top: 1px solid rgba(255,255,255,0.08);
            padding-top: 24px; display: flex; justify-content: space-between;
            align-items: center; flex-wrap: wrap; gap: 12px;
        }
        .footer-bottom p { font-size: 13px; }
        .footer-bottom a { color: var(--gold); text-decoration: none; font-weight: 600; }

        @media (max-width: 768px) {
            .footer-grid { grid-template-columns: 1fr 1fr; }
        }
        @media (max-width: 480px) {
            .footer-grid { grid-template-columns: 1fr; }
        }

        /* ===== MODAL ===== */
        .modal-overlay {
            display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
            z-index: 2000; align-items: center; justify-content: center; padding: 20px;
        }
        .modal-overlay.active { display: flex; }
        .modal {
            background: var(--white); border-radius: var(--radius); padding: 36px;
            max-width: 520px; width: 100%; max-height: 90vh; overflow-y: auto;
            position: relative; animation: modalIn 0.3s ease;
        }
        @keyframes modalIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .modal-close {
            position: absolute; top: 16px; right: 16px; background: var(--gray-100);
            border: none; width: 36px; height: 36px; border-radius: 50%;
            cursor: pointer; font-size: 18px; display: flex; align-items: center;
            justify-content: center; transition: 0.2s;
        }
        .modal-close:hover { background: var(--gray-200); }
        .modal-title { font-family: 'Playfair Display', serif; font-size: 26px; margin-bottom: 4px; }
        .modal-price { font-size: 22px; font-weight: 700; color: var(--gold); margin-bottom: 20px; }
        .modal hr { border: none; border-top: 1px solid var(--gray-200); margin: 20px 0; }
        .modal-label { font-size: 14px; font-weight: 700; margin-bottom: 12px; }

        /* Tracker color choice */
        .color-choices { display: flex; gap: 12px; margin-bottom: 8px; }
        .color-choice {
            display: flex; align-items: center; gap: 10px; padding: 10px 20px;
            border-radius: 50px; border: 2px solid var(--gray-200); cursor: pointer;
            transition: all 0.2s; font-weight: 600; font-size: 14px; background: var(--white);
        }
        .color-choice:hover { border-color: var(--navy); }
        .color-choice.selected { border-color: var(--navy); background: var(--navy); color: var(--white); }
        .color-dot { width: 20px; height: 20px; border-radius: 50%; border: 2px solid var(--gray-200); }

        /* Bracelet choice with photos */
        .bracelet-choices { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 8px; }
        .bracelet-choice {
            width: 70px; text-align: center; cursor: pointer; transition: all 0.2s;
            border: 2px solid transparent; border-radius: 12px; padding: 6px;
        }
        .bracelet-choice:hover { border-color: var(--gold); }
        .bracelet-choice.selected { border-color: var(--gold); background: rgba(212,168,83,0.08); }
        .bracelet-choice img { width: 56px; height: 56px; border-radius: 8px; object-fit: contain; }
        .bracelet-choice p { font-size: 10px; font-weight: 600; margin-top: 4px; color: var(--gray-600); }

        /* Preview image in modal */
        .modal-preview {
            width: 100%; text-align: center; margin: 16px 0;
            background: var(--gray-50); border-radius: var(--radius-sm); padding: 16px;
        }
        .modal-preview img { max-width: 180px; max-height: 180px; object-fit: contain; border-radius: 8px; }

        /* Selection summary */
        .modal-selection {
            background: var(--gray-50); border-radius: var(--radius-sm);
            padding: 14px 18px; font-size: 14px; margin: 16px 0;
        }
        .modal-selection strong { color: var(--navy); }

        .modal-whatsapp {
            display: block; width: 100%; padding: 16px; background: var(--navy);
            color: var(--white); border: none; border-radius: 50px; font-size: 16px;
            font-weight: 700; cursor: pointer; transition: all 0.25s; text-align: center;
            text-decoration: none; font-family: inherit;
        }
        .modal-whatsapp:hover { background: var(--navy-light); transform: translateY(-1px); }

        /* ===== ANIMATE ON SCROLL ===== */
        .fade-up { opacity: 0; transform: translateY(30px); transition: all 0.6s ease; }
        .fade-up.visible { opacity: 1; transform: translateY(0); }
    </style>
</head>
<body>

    <!-- NAVBAR -->
    <nav class="navbar">
        <a href="#" class="navbar-brand">
            <img src="/static/images/Guindima_Logo_blanc.png" alt="Guindima" onerror="this.style.display='none'">
            <div class="navbar-brand-text">
                <div class="navbar-brand-name">Guindima</div>
                <div class="navbar-brand-sub">by 2MK Business</div>
            </div>
        </a>
        <div class="navbar-links">
            <a href="#produits">Produits</a>
            <a href="#fonctionnement">Comment ça marche</a>
            <a href="#usages">Cas d'usage</a>
            <a href="#faq">FAQ</a>
            <a href="WHATSAPP_LINK" class="navbar-cta">
                <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.612.616l4.532-1.47A11.946 11.946 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.24 0-4.313-.724-5.996-1.95l-.418-.31-2.689.872.892-2.636-.342-.442A9.935 9.935 0 012 12C2 6.486 6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z"/></svg>
                Commander
            </a>
        </div>
        <button class="menu-toggle" onclick="toggleMenu()">
            <span></span><span></span><span></span>
        </button>
    </nav>
    <div class="mobile-menu" id="mobileMenu">
        <a href="#produits" onclick="toggleMenu()">Produits</a>
        <a href="#fonctionnement" onclick="toggleMenu()">Comment ça marche</a>
        <a href="#usages" onclick="toggleMenu()">Cas d'usage</a>
        <a href="#faq" onclick="toggleMenu()">FAQ</a>
        <a href="/guide" onclick="toggleMenu()">Guide d'utilisation</a>
        <a href="/contenu" onclick="toggleMenu()">Contenu du kit</a>
        <a href="WHATSAPP_LINK" style="background:var(--green-whatsapp);color:white;padding:12px;border-radius:50px;text-align:center;font-weight:700;">Commander sur WhatsApp</a>
    </div>

    <!-- HERO -->
    <section class="hero">
        <div class="hero-inner">
            <div class="hero-content">
                <div class="hero-badge">🇸🇳 Conçu au Sénégal</div>
                <h1>Localisez vos <em>proches</em> en temps réel</h1>
                <p>Tracker GPS compact et discret pour vos proches : enfants, parents âgés, véhicules, objets de valeur. Localisez-le en temps réel depuis votre téléphone, partout dans le monde.</p>
                <div class="hero-buttons">
                    <a href="#produits" class="btn btn-primary">Voir les produits</a>
                    <a href="#fonctionnement" class="btn btn-secondary">Comment ça marche</a>
                </div>
                <div class="hero-specs">
                    <div class="hero-spec">
                        <div class="hero-spec-value">1-2 ans</div>
                        <div class="hero-spec-label">Autonomie</div>
                    </div>
                    <div class="hero-spec">
                        <div class="hero-spec-value">4.2 cm</div>
                        <div class="hero-spec-label">Diamètre</div>
                    </div>
                    <div class="hero-spec">
                        <div class="hero-spec-value">iOS & Android</div>
                        <div class="hero-spec-label">Compatible</div>
                    </div>
                </div>
            </div>
            <div class="hero-image">
                <img src="/static/images/tracker_noir.png" alt="Tracker Guindima">
            </div>
        </div>
    </section>

    <!-- MARQUEE -->
    <div class="marquee">
        <div class="marquee-track">
            <span class="marquee-item">📍 Localisation temps réel</span>
            <span class="marquee-item">🔋 Autonomie 1-2 ans</span>
            <span class="marquee-item">📱 Compatible iOS & Android</span>
            <span class="marquee-item">🚚 Livraison 24h Dakar</span>
            <span class="marquee-item">💳 Paiement Wave & OM</span>
            <span class="marquee-item">🛡️ Garantie 30 jours</span>
            <span class="marquee-item">📍 Localisation temps réel</span>
            <span class="marquee-item">🔋 Autonomie 1-2 ans</span>
            <span class="marquee-item">📱 Compatible iOS & Android</span>
            <span class="marquee-item">🚚 Livraison 24h Dakar</span>
            <span class="marquee-item">💳 Paiement Wave & OM</span>
            <span class="marquee-item">🛡️ Garantie 30 jours</span>
        </div>
    </div>

    <!-- PRODUCTS -->
    <section class="section" id="produits">
        <div class="section-inner">
            <div class="section-header fade-up">
                <div class="section-label">NOS PRODUITS</div>
                <h2 class="section-title">Trackers, Kits & Bracelets</h2>
                <p class="section-subtitle">Choisissez le tracker seul, un kit complet ou un bracelet de remplacement.</p>
            </div>
            <div class="products-grid fade-up">
                <!-- Tracker seul -->
                <div class="product-card" onclick="openModal('tracker')">
                    <img class="product-img" src="/static/images/tracker_noir.png" alt="Tracker GPS">
                    <div class="product-name">Tracker GPS</div>
                    <div class="product-desc">Le tracker seul. Idéal pour un sac, des clés, une voiture ou si vous avez déjà un bracelet.</div>
                    <div class="product-price">9 000 F</div>
                    <ul class="product-features">
                        <li>Tracker GPS compact (4.2 cm)</li>
                        <li>Pile CR2032 incluse</li>
                        <li>Lanière de transport</li>
                        <li>Outil d'ouverture</li>
                    </ul>
                    <button class="product-btn">Choisir la couleur →</button>
                </div>
                <!-- Kit Saytu -->
                <div class="product-card popular" onclick="openModal('kit_saytu')">
                    <div class="product-badge">Populaire</div>
                    <img class="product-img" src="/static/images/silicon_watchs.png" alt="Kit Saytu">
                    <div class="product-name">Kit Saytu</div>
                    <div class="product-desc">Tracker + Bracelet Silicone. Doux et confortable avec 15 motifs colorés.</div>
                    <div class="product-price">11 500 F</div>
                    <ul class="product-features">
                        <li>Tracker GPS compact</li>
                        <li>Bracelet silicone au choix</li>
                        <li>15 motifs disponibles</li>
                        <li>Pile + accessoires inclus</li>
                    </ul>
                    <button class="product-btn">Personnaliser →</button>
                </div>
                <!-- Kit Guestu -->
                <div class="product-card" onclick="openModal('kit_guestu')">
                    <img class="product-img" src="/static/images/Nylons_bracelet.png" alt="Kit Guëstu">
                    <div class="product-name">Kit Guëstu</div>
                    <div class="product-desc">Tracker + Bracelet Nylon. Résistant et ajustable, idéal pour les actifs.</div>
                    <div class="product-price">12 500 F</div>
                    <ul class="product-features">
                        <li>Tracker GPS compact</li>
                        <li>Bracelet nylon résistant</li>
                        <li>8 couleurs disponibles</li>
                        <li>Pile + accessoires inclus</li>
                    </ul>
                    <button class="product-btn">Personnaliser →</button>
                </div>
            </div>
        </div>
    </section>

    <!-- BRACELETS CAROUSEL -->
    <section class="section bracelets-section" id="bracelets">
        <div class="section-inner">
            <div class="section-header fade-up">
                <div class="section-label">🛒 BRACELETS SEULS & GALERIE</div>
                <h2 class="section-title">Découvrez nos bracelets</h2>
                <p class="section-subtitle">Inclus dans les kits ou disponibles séparément. Cliquez pour commander.</p>
            </div>

            <!-- Silicone carousel -->
            <div class="bracelet-type fade-up">
                <div class="bracelet-type-header">
                    <div class="bracelet-type-title">Silicone</div>
                    <div class="bracelet-type-price">2 500 F l'unité</div>
                </div>
                <div class="carousel-wrapper">
                    <div class="carousel-track" id="silicone-carousel"></div>
                </div>
            </div>

            <!-- Nylon carousel -->
            <div class="bracelet-type fade-up">
                <div class="bracelet-type-header">
                    <div class="bracelet-type-title">Nylon</div>
                    <div class="bracelet-type-price">3 500 F l'unité</div>
                </div>
                <div class="carousel-wrapper">
                    <div class="carousel-track" id="nylon-carousel"></div>
                </div>
            </div>
        </div>
    </section>

    <!-- HOW IT WORKS -->
    <section class="section" id="fonctionnement">
        <div class="section-inner">
            <div class="section-header fade-up">
                <div class="section-label">COMMENT ÇA MARCHE</div>
                <h2 class="section-title">4 étapes simples</h2>
                <p class="section-subtitle">De la commande à la localisation, c'est rapide et facile.</p>
            </div>
            <div class="steps-grid fade-up">
                <div class="step">
                    <h4>Commandez</h4>
                    <p>Via WhatsApp, choisissez votre kit et personnalisez-le.</p>
                </div>
                <div class="step">
                    <h4>Recevez</h4>
                    <p>Livraison en 24h à Dakar et banlieue. Paiement Wave ou OM.</p>
                </div>
                <div class="step">
                    <h4>Connectez</h4>
                    <p>Allumez le tracker et associez-le via Find My (iOS) ou Find Hub (Android).</p>
                </div>
                <div class="step">
                    <h4>Localisez</h4>
                    <p>Suivez vos proches en temps réel depuis votre téléphone, partout dans le monde.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- FEATURES -->
    <section class="section" style="background:var(--gray-50);">
        <div class="section-inner">
            <div class="section-header fade-up">
                <div class="section-label">POURQUOI GUINDIMA</div>
                <h2 class="section-title">Tout ce qu'il faut, rien de trop</h2>
            </div>
            <div class="features-grid fade-up">
                <div class="feature-card">
                    <div class="feature-icon">📍</div>
                    <h4>Localisation GPS</h4>
                    <p>Suivez en temps réel sur votre téléphone, partout dans le monde.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📱</div>
                    <h4>iOS & Android</h4>
                    <p>Apple Find My et Google Find Hub. Compatible avec tous les smartphones.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔋</div>
                    <h4>1 à 2 ans d'autonomie</h4>
                    <p>Pile CR2032 standard, facilement remplaçable en 30 secondes.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🚚</div>
                    <h4>Livraison rapide</h4>
                    <p>Livraison en 24h à Dakar et banlieue. Paiement Wave ou Orange Money.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔔</div>
                    <h4>Alertes intelligentes</h4>
                    <p>Soyez notifié si votre proche quitte une zone définie ou si le tracker s'éloigne.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔊</div>
                    <h4>Faire sonner</h4>
                    <p>Retrouvez vos objets en faisant sonner le tracker depuis votre téléphone.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- USAGES -->
    <section class="section" id="usages">
        <div class="section-inner">
            <div class="section-header fade-up">
                <div class="section-label">CAS D'USAGE</div>
                <h2 class="section-title">Pour toutes les situations</h2>
                <p class="section-subtitle">Guindima s'adapte à votre quotidien.</p>
            </div>
            <div class="usages-grid fade-up">
                <div class="usage-card"><div class="usage-icon">👴</div><p>Personnes âgées</p></div>
                <div class="usage-card"><div class="usage-icon">👶</div><p>Enfants</p></div>
                <div class="usage-card"><div class="usage-icon">🚗</div><p>Véhicules</p></div>
                <div class="usage-card"><div class="usage-icon">🧳</div><p>Bagages</p></div>
                <div class="usage-card"><div class="usage-icon">🔑</div><p>Clés</p></div>
                <div class="usage-card"><div class="usage-icon">🎒</div><p>Sacs</p></div>
                <div class="usage-card"><div class="usage-icon">🐕</div><p>Animaux</p></div>
            </div>
        </div>
    </section>

    <!-- FAQ -->
    <section class="section" style="background:var(--gray-50);" id="faq">
        <div class="section-inner">
            <div class="section-header fade-up">
                <div class="section-label">FAQ</div>
                <h2 class="section-title">Questions fréquentes</h2>
            </div>
            <div class="faq-list fade-up">
                <div class="faq-item">
                    <button class="faq-question" onclick="toggleFaq(this)">Comment fonctionne le tracker Guindima ?</button>
                    <div class="faq-answer">Le tracker utilise les réseaux Bluetooth Find My (Apple) et Find Hub (Google) pour transmettre sa position. Il n'a pas besoin de carte SIM ni d'abonnement. Vous le connectez une seule fois à votre téléphone et vous pouvez le localiser depuis n'importe où dans le monde via l'application.</div>
                </div>
                <div class="faq-item">
                    <button class="faq-question" onclick="toggleFaq(this)">Quelle est l'autonomie de la batterie ?</button>
                    <div class="faq-answer">Le tracker fonctionne avec une pile CR2032 standard qui offre 1 à 2 ans d'autonomie selon l'utilisation. Le remplacement est simple et rapide avec l'outil d'ouverture inclus. Les piles CR2032 sont disponibles partout (pharmacies, supermarchés).</div>
                </div>
                <div class="faq-item">
                    <button class="faq-question" onclick="toggleFaq(this)">Est-ce compatible avec mon téléphone ?</button>
                    <div class="faq-answer">Oui ! Le tracker est compatible avec tous les iPhone (via l'app "Localiser" / Find My) et tous les smartphones Android (via l'app "Google Find Hub"). Il suffit d'avoir le Bluetooth activé.</div>
                </div>
                <div class="faq-item">
                    <button class="faq-question" onclick="toggleFaq(this)">Comment passer commande ?</button>
                    <div class="faq-answer">Envoyez-nous un message sur WhatsApp au +221 77 231 07 15. Choisissez votre produit, personnalisez-le (couleur du tracker, motif/couleur du bracelet) et payez via Wave ou Orange Money. Livraison en 24h à Dakar et banlieue.</div>
                </div>
                <div class="faq-item">
                    <button class="faq-question" onclick="toggleFaq(this)">Y a-t-il un abonnement mensuel ?</button>
                    <div class="faq-answer">Non, aucun abonnement. Vous payez une seule fois pour le tracker et/ou le kit. La localisation passe par les réseaux Apple Find My et Google Find Hub qui sont gratuits et illimités.</div>
                </div>
                <div class="faq-item">
                    <button class="faq-question" onclick="toggleFaq(this)">Le tracker fonctionne-t-il en dehors du Sénégal ?</button>
                    <div class="faq-answer">Oui, le tracker fonctionne partout dans le monde. Il utilise les réseaux Apple et Google qui sont disponibles mondialement. Que vous soyez à Dakar, Paris ou New York, vous pourrez localiser votre tracker.</div>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA -->
    <section class="cta-section">
        <h2>Prêt à protéger vos proches ?</h2>
        <p>Commandez maintenant et recevez votre Guindima en 24h à Dakar</p>
        <a href="WHATSAPP_LINK" class="cta-btn">
            <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.612.616l4.532-1.47A11.946 11.946 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.24 0-4.313-.724-5.996-1.95l-.418-.31-2.689.872.892-2.636-.342-.442A9.935 9.935 0 012 12C2 6.486 6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z"/></svg>
            Commander sur WhatsApp →
        </a>
        <!-- Resource links -->
        <div class="resource-links">
            <a href="/guide" class="resource-link">
                <div class="resource-link-icon">📖</div>
                <div class="resource-link-text">
                    <h4>Guide d'utilisation</h4>
                    <p>Démarrer, connecter et localiser</p>
                </div>
            </a>
            <a href="/contenu" class="resource-link">
                <div class="resource-link-icon">📦</div>
                <div class="resource-link-text">
                    <h4>Contenu du kit</h4>
                    <p>Ce qui est inclus dans chaque offre</p>
                </div>
            </a>
        </div>
    </section>

    <!-- FOOTER -->
    <footer class="footer">
        <div class="footer-inner">
            <div class="footer-grid">
                <div class="footer-brand">
                    <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                        <img src="/static/images/Guindima_Logo_dark.png" alt="Guindima" style="height:36px;border-radius:6px;" onerror="this.style.display='none'">
                        <div>
                            <h3 style="margin:0;"><span>GUINDIMA</span></h3>
                            <div style="font-size:12px;color:var(--gold);">par 2MK Business</div>
                        </div>
                    </div>
                    <p>Le tracker GPS compact pour localiser vos proches en temps réel. Conçu au Sénégal, fonctionne dans le monde entier.</p>
                    <!-- SOCIAL ICONS -->
                    <div class="footer-social">
                        <!-- TikTok -->
                        <a href="https://www.tiktok.com/@2mk_business" target="_blank" title="TikTok">
                            <svg viewBox="0 0 24 24"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1v-3.5a6.37 6.37 0 00-.79-.05A6.34 6.34 0 003.15 15.2a6.34 6.34 0 0010.86 4.46V13a8.2 8.2 0 005.58 2.18V11.7a4.83 4.83 0 01-3.77-1.78V6.69h3.77z"/></svg>
                        </a>
                        <!-- Instagram -->
                        <a href="https://www.instagram.com/2mk_business" target="_blank" title="Instagram">
                            <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
                        </a>
                        <!-- Facebook -->
                        <a href="https://www.facebook.com/profile.php?id=61574aborede" target="_blank" title="Facebook">
                            <svg viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                        </a>
                        <!-- X / Twitter -->
                        <a href="https://x.com/2mk_business" target="_blank" title="X">
                            <svg viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                        </a>
                        <!-- WhatsApp -->
                        <a href="https://wa.me/221772310715" target="_blank" title="WhatsApp">
                            <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.612.616l4.532-1.47A11.946 11.946 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.24 0-4.313-.724-5.996-1.95l-.418-.31-2.689.872.892-2.636-.342-.442A9.935 9.935 0 012 12C2 6.486 6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z"/></svg>
                        </a>
                    </div>
                </div>
                <div class="footer-col">
                    <h4>Navigation</h4>
                    <a href="#produits">Produits</a>
                    <a href="#fonctionnement">Comment ça marche</a>
                    <a href="#usages">Cas d'usage</a>
                    <a href="#faq">FAQ</a>
                </div>
                <div class="footer-col">
                    <h4>Ressources</h4>
                    <a href="/guide">Guide d'utilisation</a>
                    <a href="/contenu">Contenu du kit</a>
                </div>
                <div class="footer-col">
                    <h4>Contact</h4>
                    <div class="footer-contact-item">📱 WhatsApp : +221 77 231 07 15</div>
                    <div class="footer-contact-item">📍 Dakar, Sénégal</div>
                    <div class="footer-contact-item">🚚 Livraison 24h Dakar & banlieue</div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2026 Guindima. Une marque de <a href="#">2MK Business</a>. Tous droits réservés.</p>
            </div>
        </div>
    </footer>

    <!-- MODAL -->
    <div class="modal-overlay" id="modalOverlay" onclick="if(event.target===this)closeModal()">
        <div class="modal" id="modalContent"></div>
    </div>

    <script>
    const WHATSAPP = 'https://wa.me/221772310715';

    // Replace all WhatsApp links
    document.querySelectorAll('a[href="WHATSAPP_LINK"]').forEach(a => {
        a.href = WHATSAPP + '?text=' + encodeURIComponent('Bonjour, je suis intéressé par Guindima');
    });

    // ===== BRACELET DATA WITH INDIVIDUAL IMAGES =====
    const siliconeItems = [
        { name: "Vert Nuage", img: "/static/images/silicone/vert_nuage.png" },
        { name: "Rose Arc-en-ciel", img: "/static/images/silicone/rose_arc.png" },
        { name: "Noir Fleur", img: "/static/images/silicone/noir_fleur.png" },
        { name: "Rouge Donut", img: "/static/images/silicone/rouge_donut.png" },
        { name: "Vert Menthe Glace", img: "/static/images/silicone/vert_glace.png" },
        { name: "Rose Baleine", img: "/static/images/silicone/rose_baleine.png" },
        { name: "Mauve Licorne", img: "/static/images/silicone/mauve_licorne.png" },
        { name: "Jaune Donut", img: "/static/images/silicone/jaune_donut.png" },
        { name: "Vert Bonbon", img: "/static/images/silicone/vert_bonbon.png" },
        { name: "Rose Licorne", img: "/static/images/silicone/rose_licorne.png" },
        { name: "Bleu Saturne", img: "/static/images/silicone/bleu_saturne.png" },
        { name: "Blanc Glace", img: "/static/images/silicone/blanc_glace.png" },
        { name: "Bleu Dino", img: "/static/images/silicone/bleu_dino.png" },
        { name: "Vert Dino", img: "/static/images/silicone/vert_dino.png" },
        { name: "Beige Licorne", img: "/static/images/silicone/beige_licorne.png" }
    ];

    const nylonItems = [
        { name: "Bleu", img: "/static/images/nylon/bleu.png" },
        { name: "Blanc", img: "/static/images/nylon/blanc.png" },
        { name: "Noir", img: "/static/images/nylon/noir.png" },
        { name: "Rose Sable", img: "/static/images/nylon/rose_sable.png" },
        { name: "Rouge", img: "/static/images/nylon/rouge.png" },
        { name: "Rainbow", img: "/static/images/nylon/rainbow.png" },
        { name: "Sept Couleurs", img: "/static/images/nylon/sept_couleurs.png" },
        { name: "Jaune-Vert", img: "/static/images/nylon/jaune_vert.png" }
    ];

    // ===== CAROUSEL CREATION =====
    function createCarousel(containerId, items) {
        const container = document.getElementById(containerId);
        // Triple for seamless infinite scroll
        const allItems = [...items, ...items, ...items];
        allItems.forEach(item => {
            const div = document.createElement('div');
            div.className = 'carousel-item';
            div.onclick = (e) => {
                e.stopPropagation();
                const type = containerId.includes('silicone') ? 'bracelet_silicone' : 'bracelet_nylon';
                openModal(type, item.name);
            };
            div.innerHTML = `
                <img src="${item.img}" alt="${item.name}" onerror="this.src='/static/images/silicon_watchs.png'">
                <p>${item.name}</p>
            `;
            container.appendChild(div);
        });
    }
    createCarousel('silicone-carousel', siliconeItems);
    createCarousel('nylon-carousel', nylonItems);

    // ===== MODAL SYSTEM =====
    let currentSelection = {};

    function openModal(product, preselect) {
        const overlay = document.getElementById('modalOverlay');
        const content = document.getElementById('modalContent');
        currentSelection = { product };

        let html = '';
        if (product === 'tracker') {
            currentSelection.tracker_color = 'Noir';
            html = buildTrackerModal();
        } else if (product === 'kit_saytu') {
            currentSelection.tracker_color = 'Noir';
            currentSelection.bracelet = preselect || siliconeItems[0].name;
            html = buildKitSaytuModal();
        } else if (product === 'kit_guestu') {
            currentSelection.tracker_color = 'Noir';
            currentSelection.bracelet = preselect || nylonItems[0].name;
            html = buildKitGuestuModal();
        } else if (product === 'bracelet_silicone') {
            currentSelection.bracelet = preselect || siliconeItems[0].name;
            html = buildBraceletModal('silicone');
        } else if (product === 'bracelet_nylon') {
            currentSelection.bracelet = preselect || nylonItems[0].name;
            html = buildBraceletModal('nylon');
        }

        content.innerHTML = html;
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        updateModalPreview();
    }

    function closeModal() {
        document.getElementById('modalOverlay').classList.remove('active');
        document.body.style.overflow = '';
    }

    function selectTracker(color) {
        currentSelection.tracker_color = color;
        document.querySelectorAll('.color-choice').forEach(el => el.classList.remove('selected'));
        event.currentTarget.classList.add('selected');
        updateSelection();
    }

    function selectBracelet(name) {
        currentSelection.bracelet = name;
        document.querySelectorAll('.bracelet-choice').forEach(el => el.classList.remove('selected'));
        event.currentTarget.classList.add('selected');
        updateModalPreview();
        updateSelection();
    }

    function updateModalPreview() {
        const preview = document.getElementById('modalPreviewImg');
        if (!preview) return;
        const items = currentSelection.product.includes('nylon') || currentSelection.product === 'kit_guestu' ? nylonItems : siliconeItems;
        const found = items.find(i => i.name === currentSelection.bracelet);
        if (found) preview.src = found.img;
    }

    function updateSelection() {
        const el = document.getElementById('selectionText');
        if (!el) return;
        const parts = [];
        if (currentSelection.tracker_color) parts.push('Tracker ' + currentSelection.tracker_color);
        if (currentSelection.bracelet) parts.push('Bracelet ' + currentSelection.bracelet);
        el.textContent = parts.join(' + ');
    }

    function orderWhatsApp() {
        const parts = [];
        if (currentSelection.product === 'tracker') {
            parts.push('Tracker GPS ' + (currentSelection.tracker_color || 'Noir'));
        } else if (currentSelection.product === 'kit_saytu') {
            parts.push('Kit Saytu : Tracker ' + (currentSelection.tracker_color || 'Noir') + ' + Bracelet Silicone ' + (currentSelection.bracelet || ''));
        } else if (currentSelection.product === 'kit_guestu') {
            parts.push('Kit Guëstu : Tracker ' + (currentSelection.tracker_color || 'Noir') + ' + Bracelet Nylon ' + (currentSelection.bracelet || ''));
        } else if (currentSelection.product === 'bracelet_silicone') {
            parts.push('Bracelet Silicone : ' + (currentSelection.bracelet || ''));
        } else if (currentSelection.product === 'bracelet_nylon') {
            parts.push('Bracelet Nylon : ' + (currentSelection.bracelet || ''));
        }
        const msg = 'Bonjour, je voudrais commander : ' + parts.join(', ');
        window.open(WHATSAPP + '?text=' + encodeURIComponent(msg), '_blank');
    }

    // ===== MODAL BUILDERS =====
    function trackerColorHTML() {
        return `
            <div class="modal-label">Couleur du tracker</div>
            <div class="color-choices">
                <div class="color-choice ${currentSelection.tracker_color==='Blanc'?'selected':''}" onclick="selectTracker('Blanc')">
                    <div class="color-dot" style="background:#f0f0f0;"></div> Blanc
                </div>
                <div class="color-choice ${currentSelection.tracker_color==='Noir'?'selected':''}" onclick="selectTracker('Noir')">
                    <div class="color-dot" style="background:#1a1a1a;border-color:#333;"></div> Noir
                </div>
            </div>
        `;
    }

    function braceletChoicesHTML(items) {
        return items.map(item => `
            <div class="bracelet-choice ${currentSelection.bracelet===item.name?'selected':''}" onclick="selectBracelet('${item.name.replace(/'/g, "\\'")}')">
                <img src="${item.img}" alt="${item.name}" onerror="this.src='/static/images/silicon_watchs.png'">
                <p>${item.name}</p>
            </div>
        `).join('');
    }

    function buildTrackerModal() {
        return `
            <button class="modal-close" onclick="closeModal()">✕</button>
            <div class="modal-title">Tracker GPS</div>
            <div class="modal-price">9 000 F</div>
            <hr>
            ${trackerColorHTML()}
            <div class="modal-selection"><strong>Votre sélection :</strong> <span id="selectionText">Tracker ${currentSelection.tracker_color}</span></div>
            <button class="modal-whatsapp" onclick="orderWhatsApp()">Commander sur WhatsApp →</button>
        `;
    }

    function buildKitSaytuModal() {
        return `
            <button class="modal-close" onclick="closeModal()">✕</button>
            <div class="modal-title">Kit Saytu</div>
            <div class="modal-price">11 500 F</div>
            <hr>
            ${trackerColorHTML()}
            <div class="modal-label" style="margin-top:20px;">Motif du bracelet silicone (15 choix)</div>
            <div class="modal-preview" id="modalPreview"><img id="modalPreviewImg" src="${siliconeItems.find(i=>i.name===currentSelection.bracelet)?.img || siliconeItems[0].img}" alt="Aperçu"></div>
            <div class="bracelet-choices">${braceletChoicesHTML(siliconeItems)}</div>
            <div class="modal-selection"><strong>Votre sélection :</strong> <span id="selectionText">Tracker ${currentSelection.tracker_color} + Bracelet ${currentSelection.bracelet}</span></div>
            <button class="modal-whatsapp" onclick="orderWhatsApp()">Commander sur WhatsApp →</button>
        `;
    }

    function buildKitGuestuModal() {
        return `
            <button class="modal-close" onclick="closeModal()">✕</button>
            <div class="modal-title">Kit Guëstu</div>
            <div class="modal-price">12 500 F</div>
            <hr>
            ${trackerColorHTML()}
            <div class="modal-label" style="margin-top:20px;">Couleur du bracelet nylon (8 choix)</div>
            <div class="modal-preview" id="modalPreview"><img id="modalPreviewImg" src="${nylonItems.find(i=>i.name===currentSelection.bracelet)?.img || nylonItems[0].img}" alt="Aperçu"></div>
            <div class="bracelet-choices">${braceletChoicesHTML(nylonItems)}</div>
            <div class="modal-selection"><strong>Votre sélection :</strong> <span id="selectionText">Tracker ${currentSelection.tracker_color} + Bracelet ${currentSelection.bracelet}</span></div>
            <button class="modal-whatsapp" onclick="orderWhatsApp()">Commander sur WhatsApp →</button>
        `;
    }

    function buildBraceletModal(type) {
        const items = type === 'silicone' ? siliconeItems : nylonItems;
        const name = type === 'silicone' ? 'Bracelet Silicone' : 'Bracelet Nylon';
        const price = type === 'silicone' ? '2 500 F' : '3 500 F';
        return `
            <button class="modal-close" onclick="closeModal()">✕</button>
            <div class="modal-title">${name}</div>
            <div class="modal-price">${price}</div>
            <hr>
            <div class="modal-label">${type === 'silicone' ? 'Motif' : 'Couleur'} (${items.length} choix)</div>
            <div class="modal-preview" id="modalPreview"><img id="modalPreviewImg" src="${items.find(i=>i.name===currentSelection.bracelet)?.img || items[0].img}" alt="Aperçu"></div>
            <div class="bracelet-choices">${braceletChoicesHTML(items)}</div>
            <div class="modal-selection"><strong>Votre sélection :</strong> <span id="selectionText">Bracelet ${currentSelection.bracelet}</span></div>
            <button class="modal-whatsapp" onclick="orderWhatsApp()">Commander sur WhatsApp →</button>
        `;
    }

    // ===== FAQ TOGGLE =====
    function toggleFaq(btn) {
        const answer = btn.nextElementSibling;
        const wasActive = btn.classList.contains('active');
        document.querySelectorAll('.faq-question').forEach(q => q.classList.remove('active'));
        document.querySelectorAll('.faq-answer').forEach(a => a.classList.remove('active'));
        if (!wasActive) { btn.classList.add('active'); answer.classList.add('active'); }
    }

    // ===== MOBILE MENU =====
    function toggleMenu() {
        document.getElementById('mobileMenu').classList.toggle('active');
    }

    // ===== SCROLL ANIMATIONS =====
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); });
    }, { threshold: 0.1 });
    document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

    // Close modal on Escape
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
    </script>
</body>
</html>
'''

# ============================================================
# PAGE GUIDE D'UTILISATION
# ============================================================

GUIDE_HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guide d'utilisation - Guindima</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --navy: #1a2744; --navy-light: #2d3a54; --gold: #d4a853; --gold-light: #e8c97a;
            --white: #ffffff; --gray-50: #f8f9fa; --gray-100: #f0f2f5; --gray-200: #e2e6ea;
            --gray-400: #8c95a0; --gray-600: #5a6370; --radius: 16px; --radius-sm: 10px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'DM Sans', sans-serif; background: var(--white); color: var(--navy); line-height: 1.7; }
        .page-header {
            background: linear-gradient(145deg, var(--navy), var(--navy-light));
            padding: 40px 24px; text-align: center; color: white;
        }
        .page-header h1 { font-family: 'Playfair Display', serif; font-size: 32px; margin-bottom: 8px; }
        .page-header p { color: rgba(255,255,255,0.7); font-size: 15px; }
        .back-link {
            display: inline-flex; align-items: center; gap: 6px; color: var(--gold);
            text-decoration: none; font-weight: 600; font-size: 14px; margin-bottom: 16px;
        }
        .back-link:hover { text-decoration: underline; }

        /* Tabs */
        .tabs { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; padding: 20px 24px; max-width: 800px; margin: 0 auto; }
        .tab-btn {
            padding: 10px 18px; border-radius: 50px; border: 2px solid var(--gray-200);
            background: white; cursor: pointer; font-family: inherit; font-weight: 600;
            font-size: 14px; color: var(--navy); transition: all 0.2s;
        }
        .tab-btn:hover { border-color: var(--gold); }
        .tab-btn.active { background: var(--navy); color: white; border-color: var(--navy); }

        /* Content */
        .guide-content { max-width: 700px; margin: 0 auto; padding: 24px; }
        .tab-panel { display: none; }
        .tab-panel.active { display: block; }
        .step-card {
            background: white; border: 1px solid var(--gray-200); border-radius: var(--radius);
            padding: 28px; margin-bottom: 20px; position: relative;
        }
        .step-number {
            display: inline-flex; align-items: center; justify-content: center;
            width: 36px; height: 36px; border-radius: 50%; background: var(--gold);
            color: var(--navy); font-weight: 700; font-size: 16px; margin-bottom: 12px;
        }
        .step-card h3 { font-size: 18px; margin-bottom: 10px; }
        .step-card p, .step-card li { font-size: 14px; color: var(--gray-600); }
        .step-card ul { margin: 10px 0 0 20px; }
        .step-card li { margin-bottom: 6px; }
        .tip {
            background: rgba(212,168,83,0.1); border-left: 3px solid var(--gold);
            padding: 12px 16px; border-radius: 0 8px 8px 0; margin-top: 14px;
            font-size: 13px; color: var(--gray-600);
        }
        .warning {
            background: rgba(220,53,69,0.06); border-left: 3px solid #dc3545;
            padding: 12px 16px; border-radius: 0 8px 8px 0; margin-top: 14px;
            font-size: 13px; color: var(--gray-600);
        }
        .info {
            background: rgba(26,39,68,0.05); border-left: 3px solid var(--navy);
            padding: 12px 16px; border-radius: 0 8px 8px 0; margin-top: 14px;
            font-size: 13px; color: var(--gray-600);
        }

        /* Help CTA */
        .help-cta {
            background: linear-gradient(145deg, var(--navy), var(--navy-light));
            border-radius: var(--radius); padding: 36px; text-align: center; margin: 40px 0;
        }
        .help-cta h3 { color: white; font-size: 20px; margin-bottom: 8px; }
        .help-cta p { color: rgba(255,255,255,0.7); font-size: 14px; margin-bottom: 20px; }
        .help-cta a {
            display: inline-flex; align-items: center; gap: 8px;
            background: #25D366; color: white; padding: 12px 28px; border-radius: 50px;
            text-decoration: none; font-weight: 700; font-size: 15px;
        }

        .page-footer { text-align: center; padding: 20px; font-size: 13px; color: var(--gray-400); }
    </style>
</head>
<body>
    <div class="page-header">
        <a href="/" class="back-link">← Retour au site</a>
        <h1>📖 Guide d'utilisation</h1>
        <p>Configuration complète de votre tracker Guindima</p>
    </div>

    <div class="tabs">
        <button class="tab-btn active" onclick="showTab('iphone')">🍎 iPhone</button>
        <button class="tab-btn" onclick="showTab('android')">🤖 Android</button>
        <button class="tab-btn" onclick="showTab('localiser')">📍 Localiser</button>
        <button class="tab-btn" onclick="showTab('perdu')">🔔 Mode Perdu</button>
        <button class="tab-btn" onclick="showTab('batterie')">🔋 Batterie</button>
        <button class="tab-btn" onclick="showTab('reset')">🔄 Reset</button>
    </div>

    <div class="guide-content">
        <!-- iPhone -->
        <div class="tab-panel active" id="tab-iphone">
            <div class="step-card">
                <div class="step-number">1</div>
                <h3>🔌 Allumer le tracker</h3>
                <p>Appuyez une fois sur le bouton du tracker. Un son de démarrage indique qu'il est allumé.</p>
                <div class="tip">💡 Pour éteindre : maintenez le bouton pendant 3 secondes. Vous entendrez 2 bips.</div>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <h3>📱 Ouvrir l'app "Localiser" (Find My)</h3>
                <p>Sur votre iPhone :</p>
                <ul>
                    <li>Ouvrez l'application <strong>"Localiser"</strong> (Find My)</li>
                    <li>Appuyez sur le bouton <strong>"+"</strong> en haut</li>
                    <li>Sélectionnez <strong>"Ajouter un autre objet"</strong></li>
                    <li>Appuyez sur <strong>"Connecter"</strong></li>
                    <li>Suivez les instructions à l'écran pour finaliser</li>
                </ul>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <h3>✅ Configuration terminée !</h3>
                <p>Votre tracker est maintenant connecté. Vous pouvez :</p>
                <ul>
                    <li>Voir sa position sur la carte</li>
                    <li>Le faire sonner pour le retrouver</li>
                    <li>Activer les notifications si vous l'oubliez</li>
                </ul>
                <div class="info">ℹ️ Assurez-vous d'avoir la dernière version d'iOS, iPadOS ou macOS pour une compatibilité optimale.</div>
            </div>
        </div>

        <!-- Android -->
        <div class="tab-panel" id="tab-android">
            <div class="step-card">
                <div class="step-number">1</div>
                <h3>🔌 Allumer le tracker</h3>
                <p>Appuyez une fois sur le bouton. Un bip indique qu'il est allumé.</p>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <h3>📱 Méthode rapide (Fast Pair)</h3>
                <p>Si votre téléphone supporte Fast Pair :</p>
                <ul>
                    <li>Activez le Bluetooth et la localisation</li>
                    <li>Allumez le tracker près du téléphone</li>
                    <li>Une notification pop-up apparaîtra automatiquement</li>
                    <li>Appuyez sur <strong>"Connecter"</strong> et suivez les instructions</li>
                </ul>
                <div class="tip">💡 Si la notification n'apparaît pas, redémarrez votre téléphone et réessayez.</div>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <h3>📱 Méthode manuelle</h3>
                <p>Si la méthode rapide ne fonctionne pas :</p>
                <ul>
                    <li>Ouvrez <strong>Paramètres</strong> → <strong>Google</strong> → <strong>Tous les services</strong></li>
                    <li>Dans <strong>"Appareils connectés et partage"</strong>, sélectionnez <strong>"Appareils"</strong></li>
                    <li>Activez <strong>"Rechercher les appareils à proximité"</strong></li>
                    <li>Le tracker apparaîtra dans la liste</li>
                    <li>Appuyez dessus et suivez les instructions</li>
                </ul>
            </div>
            <div class="step-card">
                <div class="step-number">4</div>
                <h3>🗺️ Utiliser Google Find Hub</h3>
                <p>Une fois connecté, utilisez l'app <strong>"Google Find Hub"</strong> pour :</p>
                <ul>
                    <li><strong>Localiser à proximité :</strong> Appuyez sur "Jouer un son"</li>
                    <li><strong>Localiser à distance :</strong> Voir la position sur la carte</li>
                    <li><strong>Obtenir l'itinéraire :</strong> Naviguer vers sa position</li>
                </ul>
            </div>
        </div>

        <!-- Localiser -->
        <div class="tab-panel" id="tab-localiser">
            <div class="step-card">
                <div class="step-number">1</div>
                <h3>📍 Localiser à proximité</h3>
                <p>Si votre objet est près de vous :</p>
                <ul>
                    <li>Ouvrez l'app <strong>"Localiser"</strong> (iOS) ou <strong>"Google Find Hub"</strong> (Android)</li>
                    <li>Sélectionnez votre tracker</li>
                    <li>Appuyez sur <strong>"Jouer un son"</strong></li>
                    <li>Suivez le son pour le retrouver</li>
                </ul>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <h3>🗺️ Voir la dernière position connue</h3>
                <p>Si votre objet est loin, la dernière position connue s'affiche sur la carte. Appuyez sur <strong>"Itinéraire"</strong> pour naviguer vers cette position.</p>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <h3>🔔 Notifications d'oubli</h3>
                <p>Sélectionnez votre tracker → <strong>"Notifications"</strong> → Activez <strong>"Me prévenir si je laisse cet objet"</strong>.</p>
                <div class="tip">💡 Activez aussi "Me prévenir si retrouvé" pour être notifié quand un appareil Find My détecte votre tracker.</div>
            </div>
        </div>

        <!-- Mode Perdu -->
        <div class="tab-panel" id="tab-perdu">
            <div class="step-card">
                <div class="step-number">1</div>
                <h3>🚨 Activer le Mode Perdu</h3>
                <ul>
                    <li>Ouvrez l'app et sélectionnez votre tracker</li>
                    <li>Appuyez sur <strong>"Mode Perdu"</strong> puis <strong>"Activer"</strong></li>
                    <li>Entrez votre numéro de téléphone ou email</li>
                    <li>Ajoutez un message pour la personne qui trouvera l'objet</li>
                </ul>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <h3>📲 Ce qui se passe ensuite</h3>
                <ul>
                    <li>Notification dès que le tracker sera détecté par le réseau Find My</li>
                    <li>Le tracker est <strong>verrouillé</strong></li>
                    <li>"Me prévenir si retrouvé" automatiquement activé</li>
                </ul>
                <div class="warning">⚠️ En Mode Perdu, le tracker ne peut plus être associé à un nouvel appareil. Désactivez ce mode avant de le donner.</div>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <h3>🤝 Partager la localisation (Android)</h3>
                <p>Dans Google Find Hub → sélectionnez votre tracker → <strong>"Partager l'appareil"</strong>.</p>
            </div>
        </div>

        <!-- Batterie -->
        <div class="tab-panel" id="tab-batterie">
            <div class="step-card">
                <div class="step-number">1</div>
                <h3>🔋 Autonomie</h3>
                <p>Pile <strong>CR2032</strong> standard : <strong>1 à 2 ans</strong> d'autonomie. Disponible en pharmacie ou supermarché.</p>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <h3>🔧 Remplacer la pile</h3>
                <ul>
                    <li>Repérez l'encoche <strong>"OPEN"</strong> à l'arrière du tracker</li>
                    <li>Insérez l'outil d'ouverture et faites levier</li>
                    <li>Retirez l'ancienne pile CR2032</li>
                    <li>Insérez la nouvelle pile (<strong>côté + visible</strong>)</li>
                    <li>Refermez le tracker</li>
                </ul>
                <div class="tip">💡 Après le changement de pile, le tracker fonctionne directement sans reconnexion !</div>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <h3>♻️ Recyclage</h3>
                <p>Ne jetez pas les piles dans les ordures. Déposez-les dans les points de collecte. Gardez les piles hors de portée des enfants.</p>
            </div>
        </div>

        <!-- Reset -->
        <div class="tab-panel" id="tab-reset">
            <div class="step-card">
                <div class="step-number">1</div>
                <h3>📱 Supprimer de l'app (iOS)</h3>
                <ul>
                    <li>Ouvrez <strong>"Localiser"</strong></li>
                    <li>Sélectionnez votre tracker</li>
                    <li>Assurez-vous que le Mode Perdu est désactivé</li>
                    <li>Faites défiler → <strong>"Supprimer l'objet"</strong></li>
                </ul>
            </div>
            <div class="step-card">
                <div class="step-number">2</div>
                <h3>📱 Supprimer de l'app (Android)</h3>
                <ul>
                    <li>Ouvrez <strong>"Google Find Hub"</strong></li>
                    <li>Sélectionnez votre tracker → <strong>Paramètres</strong></li>
                    <li><strong>"Supprimer de Find Hub"</strong> et confirmez</li>
                </ul>
            </div>
            <div class="step-card">
                <div class="step-number">3</div>
                <h3>🔄 Réinitialisation d'usine</h3>
                <ul>
                    <li>Allumez le tracker</li>
                    <li>Appuyez rapidement <strong>5 fois</strong> sur le bouton</li>
                    <li>À la 5ème pression, <strong>maintenez</strong> jusqu'au bip</li>
                    <li>Le tracker est réinitialisé et prêt pour un nouvel appareil</li>
                </ul>
                <div class="warning">⚠️ Supprimez toujours le tracker de l'app AVANT de le réinitialiser.</div>
            </div>
            <div class="step-card">
                <div class="step-number">4</div>
                <h3>🔒 Détection de suivi indésirable</h3>
                <p>Si un iPhone détecte un tracker inconnu qui vous suit, vous recevrez une alerte. Le tracker émettra un son. Cette alerte ne se déclenche que si le tracker n'est pas connecté au téléphone de son propriétaire.</p>
            </div>
        </div>

        <!-- Help CTA -->
        <div class="help-cta">
            <h3>Besoin d'aide ?</h3>
            <p>Contactez-nous sur WhatsApp pour une assistance personnalisée</p>
            <a href="https://wa.me/221772310715?text=Bonjour%2C%20j'ai%20besoin%20d'aide%20pour%20mon%20tracker%20Guindima">💬 Demander de l'aide</a>
        </div>
    </div>

    <div class="page-footer">© 2026 Guindima par 2MK Business</div>

    <script>
    function showTab(name) {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        event.currentTarget.classList.add('active');
        document.getElementById('tab-' + name).classList.add('active');
    }
    </script>
</body>
</html>
'''

# ============================================================
# PAGE CONTENU DU KIT
# ============================================================

CONTENU_HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contenu du kit - Guindima</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --navy: #1a2744; --navy-light: #2d3a54; --gold: #d4a853;
            --white: #ffffff; --gray-50: #f8f9fa; --gray-100: #f0f2f5;
            --gray-200: #e2e6ea; --gray-400: #8c95a0; --gray-600: #5a6370;
            --radius: 16px; --radius-sm: 10px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'DM Sans', sans-serif; background: var(--gray-50); color: var(--navy); line-height: 1.7; }
        .page-header {
            background: linear-gradient(145deg, var(--navy), var(--navy-light));
            padding: 40px 24px; text-align: center; color: white;
        }
        .page-header h1 { font-family: 'Playfair Display', serif; font-size: 32px; margin-bottom: 8px; }
        .page-header p { color: rgba(255,255,255,0.7); font-size: 15px; }
        .back-link {
            display: inline-flex; align-items: center; gap: 6px; color: var(--gold);
            text-decoration: none; font-weight: 600; font-size: 14px; margin-bottom: 16px;
        }
        .back-link:hover { text-decoration: underline; }

        .content-wrapper { max-width: 700px; margin: 0 auto; padding: 24px; }

        .kit-section {
            background: white; border: 1px solid var(--gray-200); border-radius: var(--radius);
            padding: 32px; margin-bottom: 24px;
        }
        .kit-section.popular { border: 2px solid var(--gold); }
        .kit-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 8px; }
        .kit-header h2 { font-size: 22px; }
        .kit-header .price { font-size: 20px; font-weight: 700; color: var(--gold); }
        .kit-badge { background: var(--gold); color: var(--navy); padding: 4px 12px; border-radius: 50px; font-size: 12px; font-weight: 700; }

        .kit-items { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 16px; margin-bottom: 16px; }
        .kit-item { text-align: center; padding: 16px 8px; }
        .kit-item-icon { font-size: 32px; margin-bottom: 8px; }
        .kit-item h4 { font-size: 14px; margin-bottom: 4px; }
        .kit-item p { font-size: 12px; color: var(--gray-600); }

        .kit-info {
            background: rgba(26,39,68,0.04); border-left: 3px solid var(--navy);
            padding: 12px 16px; border-radius: 0 8px 8px 0; font-size: 13px; color: var(--gray-600);
        }

        .accessories-section {
            background: white; border: 1px solid var(--gray-200); border-radius: var(--radius);
            padding: 32px; margin-bottom: 24px;
        }
        .accessories-section h2 { font-size: 22px; margin-bottom: 20px; }
        .accessories-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
        .accessory-card { text-align: center; padding: 20px; background: var(--gray-50); border-radius: var(--radius-sm); }
        .accessory-card .icon { font-size: 36px; margin-bottom: 8px; }
        .accessory-card h4 { font-size: 15px; margin-bottom: 4px; }
        .accessory-card p { font-size: 13px; color: var(--gray-600); }

        .order-cta {
            background: linear-gradient(145deg, var(--navy), var(--navy-light));
            border-radius: var(--radius); padding: 36px; text-align: center; margin: 24px 0;
        }
        .order-cta h3 { color: white; font-size: 20px; margin-bottom: 8px; }
        .order-cta p { color: rgba(255,255,255,0.7); font-size: 14px; margin-bottom: 20px; }
        .order-cta a {
            display: inline-flex; align-items: center; gap: 8px;
            background: #25D366; color: white; padding: 14px 30px; border-radius: 50px;
            text-decoration: none; font-weight: 700; font-size: 15px;
        }

        .page-footer { text-align: center; padding: 20px; font-size: 13px; color: var(--gray-400); }
    </style>
</head>
<body>
    <div class="page-header">
        <a href="/" class="back-link">← Retour au site</a>
        <h1>📦 Contenu du kit</h1>
        <p>Découvrez ce qui est inclus dans chaque offre</p>
    </div>

    <div class="content-wrapper">
        <!-- Tracker Seul -->
        <div class="kit-section">
            <div class="kit-header">
                <h2>🔌 Tracker Seul — 9 000 F</h2>
            </div>
            <div class="kit-items">
                <div class="kit-item"><div class="kit-item-icon">📍</div><h4>Tracker GPS</h4><p>Traceur compact compatible iOS & Android</p></div>
                <div class="kit-item"><div class="kit-item-icon">🔋</div><h4>Pile CR2032</h4><p>Incluse et installée, 1-2 ans d'autonomie</p></div>
                <div class="kit-item"><div class="kit-item-icon">🔗</div><h4>Lanière/Cordon</h4><p>Pour attacher à vos clés, sac ou bagage</p></div>
                <div class="kit-item"><div class="kit-item-icon">🔧</div><h4>Outil d'ouverture</h4><p>Pour ouvrir le boîtier et changer la pile</p></div>
                <div class="kit-item"><div class="kit-item-icon">📄</div><h4>Notice</h4><p>Guide complet (guide français sur notre site)</p></div>
            </div>
            <div class="kit-info">ℹ️ <strong>Idéal pour :</strong> véhicules, bagages, clés, sacs, porte-monnaie, valises, et tout objet de valeur.</div>
        </div>

        <!-- Kit Saytu -->
        <div class="kit-section popular">
            <div class="kit-header">
                <h2>🦄 Kit Saytu — 11 500 F</h2>
                <span class="kit-badge">⭐ Populaire</span>
            </div>
            <div class="kit-items">
                <div class="kit-item"><div class="kit-item-icon">📍</div><h4>Tracker GPS</h4><p>Traceur compact compatible iOS & Android</p></div>
                <div class="kit-item"><div class="kit-item-icon">⌚</div><h4>Bracelet Silicone</h4><p>15 motifs colorés au choix</p></div>
                <div class="kit-item"><div class="kit-item-icon">🔋</div><h4>Pile CR2032</h4><p>Incluse, 1-2 ans d'autonomie</p></div>
                <div class="kit-item"><div class="kit-item-icon">🔗</div><h4>Lanière/Cordon</h4><p>Usage alternatif</p></div>
                <div class="kit-item"><div class="kit-item-icon">🔧</div><h4>Outil d'ouverture</h4><p>Pour changer la pile</p></div>
                <div class="kit-item"><div class="kit-item-icon">📄</div><h4>Notice</h4><p>Guide complet</p></div>
            </div>
            <div class="kit-info">ℹ️ <strong>Parfait pour les enfants !</strong> Bracelets colorés avec des motifs amusants (licornes, dinos, donuts, etc.)</div>
        </div>

        <!-- Kit Guestu -->
        <div class="kit-section">
            <div class="kit-header">
                <h2>🎨 Kit Guëstu — 12 500 F</h2>
            </div>
            <div class="kit-items">
                <div class="kit-item"><div class="kit-item-icon">📍</div><h4>Tracker GPS</h4><p>Traceur compact compatible iOS & Android</p></div>
                <div class="kit-item"><div class="kit-item-icon">⌚</div><h4>Bracelet Nylon</h4><p>8 couleurs élégantes au choix</p></div>
                <div class="kit-item"><div class="kit-item-icon">🔋</div><h4>Pile CR2032</h4><p>Incluse, 1-2 ans d'autonomie</p></div>
                <div class="kit-item"><div class="kit-item-icon">🔗</div><h4>Lanière/Cordon</h4><p>Usage alternatif</p></div>
                <div class="kit-item"><div class="kit-item-icon">🔧</div><h4>Outil d'ouverture</h4><p>Pour changer la pile</p></div>
                <div class="kit-item"><div class="kit-item-icon">📄</div><h4>Notice</h4><p>Guide complet</p></div>
            </div>
            <div class="kit-info">ℹ️ <strong>Bracelet nylon</strong> confortable et ajustable, idéal pour les enfants plus grands et les adultes.</div>
        </div>

        <!-- Bracelets seuls -->
        <div class="accessories-section">
            <h2>🛒 Bracelets seuls (accessoires)</h2>
            <div class="accessories-grid">
                <div class="accessory-card">
                    <div class="icon">🦄</div>
                    <h4>Bracelet Silicone</h4>
                    <p>2 500 F — 15 motifs disponibles</p>
                </div>
                <div class="accessory-card">
                    <div class="icon">🎨</div>
                    <h4>Bracelet Nylon</h4>
                    <p>3 500 F — 8 couleurs disponibles</p>
                </div>
            </div>
            <div class="kit-info">ℹ️ Achetez des bracelets supplémentaires pour changer de style ou remplacer un bracelet usé.</div>
        </div>

        <!-- Order CTA -->
        <div class="order-cta">
            <h3>Prêt à commander ?</h3>
            <p>Contactez-nous sur WhatsApp pour passer commande</p>
            <a href="https://wa.me/221772310715?text=Bonjour%2C%20je%20veux%20commander%20un%20kit%20Guindima">📱 Commander maintenant</a>
        </div>
    </div>

    <div class="page-footer">© 2026 Guindima par 2MK Business</div>
</body>
</html>
'''

# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def home():
    return render_template_string(SITE_HTML)

@app.route('/guide')
def guide():
    return render_template_string(GUIDE_HTML)

@app.route('/contenu')
def contenu():
    return render_template_string(CONTENU_HTML)

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'guindima-v2'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
