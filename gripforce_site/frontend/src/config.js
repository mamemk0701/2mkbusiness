// Configuration centralisée des produits et du site

export const SITE = {
  name: 'GripForce',
  tagline: 'Entraîne ta poigne. Réveille tes avant-bras.',
  description:
    "L'exerciseur de main compact qui renforce doigts, poignets et avant-bras. Conçu à Dakar, pensé pour ta vie quotidienne.",
  domain: 'grip.2mkbusiness.org',
  brand: '2MK Business',
  whatsapp: {
    // Numéro WhatsApp au format international sans + ni espaces
    number: '221767593281',
    displayNumber: '+221 76 759 32 81',
  },
  social: {
    tiktok: 'https://www.tiktok.com/@gripforce.sn',
    instagram: 'https://www.instagram.com/gripforce.sn',
    facebook: 'https://www.facebook.com/gripforce.sn',
  },
};

export const LAUNCH_OFFER = {
  active: true,
  label: 'Offre de lancement',
  description: 'Les 15 premiers clients',
  remaining: 15, // à mettre à jour manuellement ou via API
  deliveryFree: true,
};

export const PRODUCTS = [
  {
    id: 'gripforce-noir',
    slug: 'gripforce-noir',
    name: 'GripForce Noir',
    color: 'Noir',
    colorHex: '#1A1A18',
    priceNormal: 5500,
    priceLaunch: 4500,
    priceOld: 6500, // prix barré pour effet d'ancrage
    stock: 20,
    images: [
      '/products/gripforce-noir-1.webp',
      '/products/gripforce-noir-2.webp',
      '/products/gripforce-noir-3.webp',
    ],
    featured: true,
    description:
      "Renforce ta poigne avec style. Silicone haut de gamme, picots massants, 6 points de préhension indépendants pour chaque doigt.",
  },
  {
    id: 'gripforce-rose',
    slug: 'gripforce-rose',
    name: 'GripForce Rose',
    color: 'Rose',
    colorHex: '#F4C0D1',
    priceNormal: 5500,
    priceLaunch: 4500,
    priceOld: 6500,
    stock: 10, // disponible en rose
    images: [
      '/products/gripforce-rose-1.webp',
      '/products/gripforce-rose-2.webp',
    ],
    featured: false,
    description:
      "L'édition couleur. Même performance, look unique. Parfaite pour offrir ou pour celles qui veulent marquer leur style.",
  },
];

export const BENEFITS = [
  {
    title: 'Renforcement complet',
    description:
      "Travaille chaque doigt individuellement grâce aux 6 points de préhension. Doigts, poignets, avant-bras - tout est sollicité en 5 minutes.",
    metric: '6 pts',
    metricLabel: 'de préhension',
  },
  {
    title: 'Massage d\'acupression',
    description:
      "Les picots texturés stimulent les points d'acupression de la paume. Soulage les tensions après une journée au clavier ou au volant.",
    metric: '40+',
    metricLabel: 'picots massants',
  },
  {
    title: 'Anti-stress au quotidien',
    description:
      "Presser, relâcher, masser. Un geste simple et répétitif qui libère les tensions mentales, canalise le stress et t'aide à te recentrer.",
    metric: '5 min',
    metricLabel: 'pour décompresser',
  },
  {
    title: 'Compact et discret',
    description:
      "Se glisse dans ta sacoche, ta boîte à gants, ton tiroir de bureau. Utilisable partout : bureau, voiture, canapé, salle d'attente.",
    metric: '12 cm',
    metricLabel: 'de diamètre',
  },
];

export const USE_CASES = [
  { title: 'Sportifs', subtitle: 'Musculation · Escalade · Tennis · Arts martiaux' },
  { title: 'Bureau', subtitle: 'Devs · Designers · Étudiants' },
  { title: 'Rééducation', subtitle: 'Post-fracture · Arthrose · Syndrome canal carpien' },
  { title: 'Seniors', subtitle: 'Maintien dextérité · Force de préhension' },
  { title: 'Musiciens', subtitle: 'Guitaristes · Pianistes · Batteurs' },
  { title: 'Conducteurs', subtitle: 'Chauffeurs · Taxis · VTC' },
];

export const SPECS = [
  { label: 'Dimensions', value: '12,3 × 10 × 7 cm' },
  { label: 'Matériau', value: 'Silicone médical' },
  { label: 'Poids', value: '180 g' },
  { label: 'Points de préhension', value: '6' },
  { label: 'Résistance', value: 'Progressive' },
  { label: 'Garantie', value: '30 jours' },
];

export const FAQ = [
  {
    q: 'Le produit convient-il aux débutants ?',
    a: "Oui. La résistance est progressive et adaptée à tous les niveaux. Tu peux commencer par des séances courtes (2-3 min) et augmenter selon ta progression.",
  },
  {
    q: 'Combien de temps d\'utilisation par jour ?',
    a: "5 à 10 minutes par jour suffisent pour voir des résultats en 2-3 semaines. Tu peux l'utiliser pendant que tu regardes un film ou dans les transports.",
  },
  {
    q: 'Est-ce bruyant ?',
    a: "Non, c'est totalement silencieux. Parfait pour l'utiliser au bureau, pendant une réunion en ligne ou même la nuit.",
  },
  {
    q: 'Livraison à Dakar ?',
    a: "Livraison sous 24h à Dakar et banlieue. Pour les 15 premières commandes, la livraison est offerte.",
  },
  {
    q: 'Comment je paie ?',
    a: "Paiement par Wave ou Orange Money. Après ta commande sur WhatsApp, on te communique les numéros de paiement et on livre dès réception.",
  },
  {
    q: 'Garantie ?',
    a: "30 jours satisfait ou remboursé. Si le produit ne te convient pas ou présente un défaut, on le remplace ou on te rembourse.",
  },
];
