from flask import Flask, render_template_string
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sourire-eclat-secret-2026')

# Page d'accueil
HOME_PAGE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SourireÉclat - Bandelettes Blanchissantes | Sourire Éclatant</title>
    <meta name="description" content="Bandelettes blanchissantes SourireÉclat - Technologie PAP+ et correction violette. Résultat dès la 1ère utilisation. Livraison Dakar et tout le Sénégal.">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif;
            background: linear-gradient(135deg, #f8f0ff 0%, #e9d9ff 100%);
            color: #1a1a2e;
            line-height: 1.5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 24px;
        }
        
        .header {
            padding: 20px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            border-bottom: 2px solid rgba(139, 0, 255, 0.15);
        }
        
        .logo h1 {
            font-size: 32px;
            background: linear-gradient(135deg, #8B00FF, #5a0a9e);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        .logo span {
            font-size: 14px;
            color: #8B00FF;
            display: block;
            letter-spacing: 1px;
        }
        
        .nav {
            display: flex;
            gap: 32px;
        }
        
        .nav a {
            text-decoration: none;
            color: #4a4a6a;
            font-weight: 600;
            transition: color 0.3s;
        }
        
        .nav a:hover {
            color: #8B00FF;
        }
        
        .hero {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 50px;
            align-items: center;
            padding: 60px 0;
        }
        
        .hero-content h1 {
            font-size: 52px;
            font-weight: 800;
            background: linear-gradient(135deg, #8B00FF, #4B0082);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 16px;
        }
        
        .hero-badge {
            display: inline-block;
            background: #8B00FF20;
            color: #8B00FF;
            padding: 8px 20px;
            border-radius: 40px;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 24px;
        }
        
        .hero-features {
            display: flex;
            gap: 20px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        
        .feature {
            background: white;
            padding: 12px 20px;
            border-radius: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .feature strong {
            color: #8B00FF;
            font-size: 22px;
            display: block;
        }
        
        .btn {
            display: inline-block;
            background: linear-gradient(135deg, #8B00FF, #6A0DAD);
            color: white;
            padding: 14px 36px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 700;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 6px 16px rgba(139,0,255,0.3);
            margin-top: 20px;
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(139,0,255,0.4);
        }
        
        .hero-images {
            display: flex;
            gap: 20px;
            justify-content: center;
        }
        
        .hero-images img {
            width: 48%;
            border-radius: 20px;
            box-shadow: 0 20px 35px rgba(0,0,0,0.15);
            transition: transform 0.3s;
        }
        
        .hero-images img:hover {
            transform: scale(1.02);
        }
        
        .tech-section {
            background: white;
            border-radius: 32px;
            padding: 50px 40px;
            margin: 40px 0;
            text-align: center;
        }
        
        .tech-section h2 {
            font-size: 32px;
            margin-bottom: 40px;
        }
        
        .tech-section h2 span {
            color: #8B00FF;
        }
        
        .tech-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
        }
        
        .tech-card {
            padding: 25px;
            background: #faf5ff;
            border-radius: 20px;
            transition: all 0.3s;
        }
        
        .tech-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(139,0,255,0.1);
        }
        
        .tech-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }
        
        .tech-card h3 {
            color: #8B00FF;
            margin-bottom: 12px;
        }
        
        .cert-section {
            background: linear-gradient(135deg, #1a1a2e, #2a1a4e);
            border-radius: 32px;
            padding: 50px 40px;
            margin: 40px 0;
            text-align: center;
            color: white;
        }
        
        .cert-section h2 {
            font-size: 32px;
            margin-bottom: 15px;
        }
        
        .cert-section p {
            margin-bottom: 30px;
            opacity: 0.9;
        }
        
        .cert-section img {
            max-width: 100%;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .footer {
            background: #1a1a2e;
            color: #aaa;
            padding: 40px 0;
            margin-top: 60px;
            text-align: center;
        }
        
        @media (max-width: 768px) {
            .hero {
                grid-template-columns: 1fr;
                text-align: center;
            }
            .hero-content h1 {
                font-size: 36px;
            }
            .hero-features {
                justify-content: center;
            }
            .nav {
                margin-top: 15px;
                gap: 20px;
                flex-wrap: wrap;
            }
            .header {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <h1>😁 SourireÉclat</h1>
                <span>Bandelettes blanchissantes</span>
            </div>
            <div class="nav">
                <a href="/">Accueil</a>
                <a href="/guide">Guide</a>
                <a href="/contenu">Le Kit</a>
                <a href="/certifications">Certifications</a>
            </div>
        </div>
        
        <div class="hero">
            <div class="hero-content">
                <div class="hero-badge">✨ Technologie avancée de correction des couleurs</div>
                <h1>Blanchiment dentaire<br>PURPLE</h1>
                <div class="hero-features">
                    <div class="feature"><strong>✨ Dès la 1ʳᵉ utilisation</strong></div>
                    <div class="feature"><strong>⏱️ 30 min</strong> d'application</div>
                </div>
                <p style="margin: 20px 0; color: #444;">Les bandelettes SourireÉclat combinent correction violette et blanchiment PAP+ pour un sourire éclatant, sans sensibilité.</p>
                <a href="https://wa.me/221772310715?text=Bonjour%20Sourire%C3%89clat%2C%20je%20souhaite%20commander%20vos%20bandelettes%20blanchissantes" class="btn" target="_blank">🛒 Commander sur WhatsApp →</a>
            </div>
            <div class="hero-images">
                <img src="/static/images/1.png" alt="SourireÉclat bandelette">
                <img src="/static/images/2.png" alt="SourireÉclat packaging">
            </div>
        </div>
        
        <div class="tech-section">
            <h2>Technologie <span>double action</span></h2>
            <div class="tech-grid">
                <div class="tech-card">
                    <div class="tech-icon">🎨</div>
                    <h3>Correction Violette</h3>
                    <p>Neutralise instantanément les tons jaunes pour un sourire plus blanc dès la pose.</p>
                </div>
                <div class="tech-card">
                    <div class="tech-icon">⚗️</div>
                    <h3>PAP+ Whitening</h3>
                    <p>Formule sans peroxyde • Zéro sensibilité • Blanchiment profond et durable.</p>
                </div>
                <div class="tech-card">
                    <div class="tech-icon">🧪</div>
                    <h3>Dual-Active</h3>
                    <p>Deux technologies complémentaires pour un résultat visible et naturel.</p>
                </div>
            </div>
        </div>
        
        <div class="cert-section">
            <h2>📜 Certifications internationales</h2>
            <p>Reconnu dans plus de 100 pays • Qualité et sécurité garanties</p>
            <img src="/static/images/image.png" alt="Certificats SourireÉclat - FDA, CE, ISO13485, CPNP">
        </div>
    </div>
    
    <div class="footer">
        <div class="container">
            <p>© 2026 SourireÉclat • Livraison partout au Sénégal</p>
            <p style="margin-top: 10px; font-size: 13px;">📞 Contact : +221 77 231 07 15</p>
        </div>
    </div>
</body>
</html>
'''

# Guide d'utilisation
GUIDE_PAGE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guide - SourireÉclat</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #f8f0ff, #e9d9ff); line-height: 1.6; }
        .container { max-width: 1000px; margin: 0 auto; padding: 0 24px; }
        .header { padding: 20px 0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; border-bottom: 2px solid rgba(139,0,255,0.15); }
        .logo h1 { font-size: 28px; background: linear-gradient(135deg, #8B00FF, #5a0a9e); -webkit-background-clip: text; background-clip: text; color: transparent; }
        .nav { display: flex; gap: 30px; }
        .nav a { text-decoration: none; color: #4a4a6a; font-weight: 600; }
        .nav a:hover { color: #8B00FF; }
        .guide-card { background: white; border-radius: 32px; padding: 40px; margin: 40px 0; }
        .guide-card h1 { color: #8B00FF; margin-bottom: 30px; }
        .step { display: flex; gap: 20px; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee; }
        .step-number { width: 50px; height: 50px; background: #8B00FF; color: white; border-radius: 30px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; flex-shrink: 0; }
        .step h3 { color: #8B00FF; margin-bottom: 8px; }
        .tip { background: #faf5ff; padding: 20px; border-radius: 20px; margin-top: 30px; border-left: 4px solid #8B00FF; }
        .footer { background: #1a1a2e; color: #aaa; padding: 40px 0; margin-top: 60px; text-align: center; }
        @media (max-width: 768px) { .step { flex-direction: column; text-align: center; } .step-number { margin: 0 auto; } .header { flex-direction: column; gap: 15px; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo"><h1>😁 SourireÉclat</h1></div>
            <div class="nav">
                <a href="/">Accueil</a>
                <a href="/guide">Guide</a>
                <a href="/contenu">Le Kit</a>
                <a href="/certifications">Certifications</a>
            </div>
        </div>
        <div class="guide-card">
            <h1>📖 Guide d'utilisation</h1>
            <div class="step"><div class="step-number">1</div><div><h3>Préparez vos dents</h3><p>Brossez-vous les dents et séchez-les légèrement avec une serviette propre. Des dents propres = meilleure adhésion.</p></div></div>
            <div class="step"><div class="step-number">2</div><div><h3>Appliquez la bandelette</h3><p>Retirez la bandelette de son film. Appliquez le gel sur la face interne. Placez-la sur vos dents en appuyant doucement.</p></div></div>
            <div class="step"><div class="step-number">3</div><div><h3>Laissez agir 30 minutes</h3><p>Pendant l'application, évitez de boire, manger ou fumer. Vous pouvez vaquer à vos activités normalement.</p></div></div>
            <div class="step"><div class="step-number">4</div><div><h3>Retirez et rincez</h3><p>Après 30 minutes, retirez délicatement. Rincez-vous la bouche à l'eau tiède.</p></div></div>
            <div class="tip"><strong>💡 Conseil SourireÉclat</strong><br>✔️ Utilisez 1 fois par jour pendant 7 jours pour un résultat optimal<br>✔️ Sensibilité dentaire possible → espacez les applications<br>✔️ Conservez dans un endroit frais et sec</div>
        </div>
    </div>
    <div class="footer"><div class="container"><p>© 2026 SourireÉclat • Blanchiment dentaire professionnel à domicile</p></div></div>
</body>
</html>
'''

# Contenu du kit
CONTENU_PAGE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Le Kit - SourireÉclat</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #f8f0ff, #e9d9ff); line-height: 1.6; }
        .container { max-width: 1000px; margin: 0 auto; padding: 0 24px; }
        .header { padding: 20px 0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; border-bottom: 2px solid rgba(139,0,255,0.15); }
        .logo h1 { font-size: 28px; background: linear-gradient(135deg, #8B00FF, #5a0a9e); -webkit-background-clip: text; background-clip: text; color: transparent; }
        .nav { display: flex; gap: 30px; }
        .nav a { text-decoration: none; color: #4a4a6a; font-weight: 600; }
        .nav a:hover { color: #8B00FF; }
        .content-card { background: white; border-radius: 32px; padding: 40px; margin: 40px 0; }
        .content-card h1 { color: #8B00FF; margin-bottom: 20px; }
        .ingredient { background: #faf5ff; padding: 16px; margin: 16px 0; border-radius: 16px; border-left: 4px solid #8B00FF; }
        .footer { background: #1a1a2e; color: #aaa; padding: 40px 0; margin-top: 60px; text-align: center; }
        @media (max-width: 768px) { .header { flex-direction: column; gap: 15px; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo"><h1>😁 SourireÉclat</h1></div>
            <div class="nav">
                <a href="/">Accueil</a>
                <a href="/guide">Guide</a>
                <a href="/contenu">Le Kit</a>
                <a href="/certifications">Certifications</a>
            </div>
        </div>
        <div class="content-card">
            <h1>📦 Ce que contient votre kit</h1>
            <div class="ingredient"><h3>🎨 14 bandelettes blanchissantes</h3><p>(7 utilisations) • Infusées au gel PAP+ et correction violette</p></div>
            <div class="ingredient"><h3>📋 Guide d'utilisation illustré</h3><p>Instructions simples en français</p></div>
            <div class="ingredient"><h3>🔬 Technologie PAP+ sans peroxyde</h3><p>Zéro sensibilité • Blanchiment en douceur</p></div>
            <div class="ingredient"><h3>✨ Résultat visible dès la 1ʳᵉ fois</h3><p>Neutralise les tons jaunes • Sourire plus éclatant</p></div>
        </div>
    </div>
    <div class="footer"><div class="container"><p>© 2026 SourireÉclat • Livraison Dakar et tout le Sénégal</p></div></div>
</body>
</html>
'''

# Certifications
CERTIF_PAGE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Certifications - SourireÉclat</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #f8f0ff, #e9d9ff); }
        .container { max-width: 1000px; margin: 0 auto; padding: 0 24px; }
        .header { padding: 20px 0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; border-bottom: 2px solid rgba(139,0,255,0.15); }
        .logo h1 { font-size: 28px; background: linear-gradient(135deg, #8B00FF, #5a0a9e); -webkit-background-clip: text; background-clip: text; color: transparent; }
        .nav { display: flex; gap: 30px; }
        .nav a { text-decoration: none; color: #4a4a6a; font-weight: 600; }
        .nav a:hover { color: #8B00FF; }
        .certif-card { background: white; border-radius: 32px; padding: 40px; margin: 40px 0; text-align: center; }
        .certif-card h1 { color: #8B00FF; margin-bottom: 15px; }
        .certif-card p { margin-bottom: 30px; color: #555; }
        .certif-card img { max-width: 100%; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .badge-list { display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-top: 30px; }
        .badge { background: #f0e6ff; padding: 8px 20px; border-radius: 40px; color: #8B00FF; font-weight: 600; font-size: 14px; }
        .footer { background: #1a1a2e; color: #aaa; padding: 40px 0; margin-top: 60px; text-align: center; }
        @media (max-width: 768px) { .header { flex-direction: column; gap: 15px; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo"><h1>😁 SourireÉclat</h1></div>
            <div class="nav">
                <a href="/">Accueil</a>
                <a href="/guide">Guide</a>
                <a href="/contenu">Le Kit</a>
                <a href="/certifications">Certifications</a>
            </div>
        </div>
        <div class="certif-card">
            <h1>🌍 Reconnaissance mondiale</h1>
            <p>SourireÉclat est certifié dans plus de 100 pays et répond aux normes internationales de sécurité et de qualité.</p>
            <img src="/static/images/image.png" alt="Certificats SourireÉclat - FDA, CE, ISO13485, CPNP">
            <div class="badge-list">
                <span class="badge">FDA</span><span class="badge">CE</span><span class="badge">UKCA</span>
                <span class="badge">ISO 13485</span><span class="badge">CPNP</span><span class="badge">FC</span>
            </div>
        </div>
    </div>
    <div class="footer"><div class="container"><p>© 2026 SourireÉclat • Qualité certifiée</p></div></div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HOME_PAGE)

@app.route('/guide')
def guide():
    return render_template_string(GUIDE_PAGE)

@app.route('/contenu')
def contenu():
    return render_template_string(CONTENU_PAGE)

@app.route('/certifications')
def certifications():
    return render_template_string(CERTIF_PAGE)

@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'sourire-eclat-site'}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5004, debug=False)
