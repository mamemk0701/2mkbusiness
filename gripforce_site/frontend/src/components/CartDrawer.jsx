import { useEffect, useState } from 'react';
import { useStore } from '@nanostores/react';
import { X, Plus, Minus, Trash2, ShoppingBag } from 'lucide-react';
import { $cart, $cartTotal, updateQuantity, removeFromCart } from '../stores/cart.js';
import { SITE, LAUNCH_OFFER } from '../config.js';

export default function CartDrawer() {
  const [open, setOpen] = useState(false);
  const cart = useStore($cart);
  const total = useStore($cartTotal);

  useEffect(() => {
    const handleOpen = () => setOpen(true);
    window.addEventListener('cart:open', handleOpen);
    return () => window.removeEventListener('cart:open', handleOpen);
  }, []);

  // Prevent body scroll when open
  useEffect(() => {
    if (open) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [open]);

  const handleCheckout = () => {
    // Construire le message WhatsApp
    const lines = [
      '🛒 *Nouvelle commande GripForce*',
      '',
      '*Articles :*',
      ...cart.map(
        (item) =>
          `• ${item.name} — ${item.quantity} × ${item.price.toLocaleString('fr-FR')} F = ${(item.price * item.quantity).toLocaleString('fr-FR')} F`
      ),
      '',
      `*Sous-total :* ${total.toLocaleString('fr-FR')} FCFA`,
      LAUNCH_OFFER.active && LAUNCH_OFFER.deliveryFree
        ? '🎁 *Livraison offerte* (offre de lancement)'
        : '📦 Livraison : à définir',
      '',
      '*Mes infos :*',
      '👤 Nom : ',
      '📍 Zone de livraison : ',
      '🏠 Adresse : ',
      '',
      'Merci !',
    ].filter(Boolean);

    const message = encodeURIComponent(lines.join('\n'));
    const url = `https://wa.me/${SITE.whatsapp.number}?text=${message}`;
    window.open(url, '_blank');
  };

  return (
    <>
      {/* Backdrop */}
      <div
        className={`fixed inset-0 bg-ink-900/40 dark:bg-ink-900/60 backdrop-blur-sm z-[60] transition-opacity duration-300 ${
          open ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
        onClick={() => setOpen(false)}
        aria-hidden="true"
      />

      {/* Drawer */}
      <aside
        className={`fixed top-0 right-0 bottom-0 w-full max-w-md bg-ink-50 dark:bg-ink-900 z-[70] shadow-2xl transition-transform duration-400 ease-[cubic-bezier(0.22,1,0.36,1)] flex flex-col ${
          open ? 'translate-x-0' : 'translate-x-full'
        }`}
        aria-label="Panier"
        aria-hidden={!open}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-5 border-b border-ink-200 dark:border-ink-700">
          <div>
            <div className="font-mono text-[10px] uppercase tracking-[0.2em] text-ink-500 dark:text-ink-400">
              Votre panier
            </div>
            <h2 className="font-display text-2xl font-medium leading-tight mt-0.5">
              {cart.length} {cart.length > 1 ? 'articles' : 'article'}
            </h2>
          </div>
          <button
            onClick={() => setOpen(false)}
            aria-label="Fermer le panier"
            className="w-9 h-9 rounded-full border border-ink-200 dark:border-ink-700 hover:border-ink-400 dark:hover:border-ink-500 transition-colors flex items-center justify-center"
          >
            <X size={16} />
          </button>
        </div>

        {/* Contenu */}
        {cart.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center px-6 py-12 text-center">
            <div className="w-16 h-16 rounded-full bg-ink-100 dark:bg-ink-800 flex items-center justify-center mb-4">
              <ShoppingBag size={24} className="text-ink-400" />
            </div>
            <h3 className="font-display text-xl font-medium mb-2">Panier vide</h3>
            <p className="text-sm text-ink-500 dark:text-ink-400 max-w-xs">
              Ajoute GripForce à ton panier pour commencer ton entraînement.
            </p>
            <button
              onClick={() => setOpen(false)}
              className="btn-primary mt-6"
            >
              Voir le produit
            </button>
          </div>
        ) : (
          <>
            {/* Items */}
            <div className="flex-1 overflow-y-auto px-6 py-4">
              {cart.map((item) => (
                <div
                  key={item.id}
                  className="flex gap-4 py-4 border-b border-ink-200 dark:border-ink-700 last:border-0"
                >
                  <div className="w-20 h-20 rounded-lg bg-ink-100 dark:bg-ink-800 flex items-center justify-center overflow-hidden flex-shrink-0">
                    {item.image ? (
                      <img src={item.image} alt={item.name} className="w-full h-full object-cover" />
                    ) : (
                      <div className="w-12 h-12 rounded-full" style={{ background: item.colorHex || '#1A1A18' }} />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-medium text-sm leading-tight">{item.name}</h4>
                    <p className="text-xs text-ink-500 dark:text-ink-400 mt-0.5">
                      {item.color}
                    </p>
                    <div className="flex items-center justify-between mt-2">
                      <div className="flex items-center gap-1 border border-ink-200 dark:border-ink-700 rounded-full">
                        <button
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                          className="w-7 h-7 flex items-center justify-center hover:bg-ink-100 dark:hover:bg-ink-800 rounded-full transition-colors"
                          aria-label="Diminuer la quantité"
                        >
                          <Minus size={12} />
                        </button>
                        <span className="text-sm font-medium w-6 text-center tabular-nums">
                          {item.quantity}
                        </span>
                        <button
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                          className="w-7 h-7 flex items-center justify-center hover:bg-ink-100 dark:hover:bg-ink-800 rounded-full transition-colors"
                          aria-label="Augmenter la quantité"
                        >
                          <Plus size={12} />
                        </button>
                      </div>
                      <span className="text-sm font-semibold tabular-nums">
                        {(item.price * item.quantity).toLocaleString('fr-FR')} F
                      </span>
                    </div>
                  </div>
                  <button
                    onClick={() => removeFromCart(item.id)}
                    className="self-start w-7 h-7 rounded-full hover:bg-ink-100 dark:hover:bg-ink-800 flex items-center justify-center transition-colors text-ink-400 hover:text-alert"
                    aria-label="Supprimer l'article"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              ))}
            </div>

            {/* Footer */}
            <div className="border-t border-ink-200 dark:border-ink-700 px-6 py-5 space-y-4 bg-ink-100/50 dark:bg-ink-800/50">
              <div className="flex items-baseline justify-between">
                <span className="text-sm text-ink-500 dark:text-ink-400">Sous-total</span>
                <span className="font-display text-2xl font-medium tabular-nums">
                  {total.toLocaleString('fr-FR')} <span className="text-sm font-sans text-ink-500">FCFA</span>
                </span>
              </div>
              {LAUNCH_OFFER.active && LAUNCH_OFFER.deliveryFree && (
                <div className="flex items-center gap-2 text-xs text-success">
                  <div className="w-1.5 h-1.5 rounded-full bg-success" />
                  Livraison offerte · offre de lancement
                </div>
              )}
              <button onClick={handleCheckout} className="btn-whatsapp w-full">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.84 12.84 0 00-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.464 3.488"/>
                </svg>
                Commander via WhatsApp
              </button>
              <p className="text-[11px] text-center text-ink-500 dark:text-ink-400 leading-relaxed">
                Tu seras redirigé vers WhatsApp avec ta commande pré-remplie. On confirme avec toi et t'envoie les infos de paiement Wave / Orange Money.
              </p>
            </div>
          </>
        )}
      </aside>
    </>
  );
}
