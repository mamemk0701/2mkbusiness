# GripForce Frontend

Site e-commerce GripForce by 2MK Business, built with Astro + Tailwind + React.

## Stack

- **Astro 4** — framework statique ultra-rapide
- **Tailwind CSS** — styling utility-first
- **React 18** — composants interactifs (panier, toggle dark/light)
- **Nanostores** — state management minimaliste avec persistance localStorage
- **Lucide React** — icônes

## Structure

```
src/
├── pages/         # Routes (index, cgv, livraison)
├── components/    # Composants Astro + React
├── layouts/       # BaseLayout avec SEO + dark mode
├── stores/        # État panier (nanostores)
├── styles/        # CSS global
└── config.js      # Config centralisée (produits, prix, site info)
```

## Développement local

```bash
npm install
npm run dev
```

Le serveur démarre sur http://localhost:4321

## Build production

```bash
npm run build
```

Le build statique est généré dans `dist/`.

## Configuration

Éditer `src/config.js` pour :
- Modifier le numéro WhatsApp
- Ajuster les prix (normal / lancement)
- Activer/désactiver l'offre de lancement
- Modifier le nombre de places restantes
- Ajouter/supprimer des produits
- Mettre à jour la FAQ

## Dark mode

Le toggle dark/light est dans le header. La préférence est sauvegardée dans `localStorage` sous la clé `gripforce_theme`.

## Panier

Le panier persiste dans `localStorage` sous la clé `gripforce_cart`. Le checkout redirige vers WhatsApp avec un message pré-rempli contenant le récapitulatif de commande.
