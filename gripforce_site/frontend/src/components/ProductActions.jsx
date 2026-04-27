import { useState } from 'react';
import { Plus, Minus, Check } from 'lucide-react';
import { addToCart } from '../stores/cart.js';

export default function ProductActions({ products, price }) {
  const [selectedColor, setSelectedColor] = useState(products[0].color);
  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(false);

  const selected = products.find((p) => p.color === selectedColor) || products[0];

  const handleAdd = () => {
    addToCart({
      id: selected.id,
      name: selected.name,
      color: selected.color,
      colorHex: selected.colorHex,
      price: price,
      quantity,
    });
    setAdded(true);
    setTimeout(() => setAdded(false), 2000);
    setTimeout(() => {
      window.dispatchEvent(new CustomEvent('cart:open'));
    }, 300);
  };

  return (
    <div className="space-y-5">
      {/* Sélecteur de couleur */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm text-ink-600 dark:text-ink-300">
            Couleur : <span className="font-medium text-ink-900 dark:text-ink-50">{selectedColor}</span>
          </span>
        </div>
        <div className="flex gap-3">
          {products.map((p) => (
            <button
              key={p.color}
              onClick={() => setSelectedColor(p.color)}
              aria-label={`Sélectionner la couleur ${p.color}`}
              className={`group relative w-14 h-14 rounded-full border-2 transition-all ${
                selectedColor === p.color
                  ? 'border-volt-500 scale-105'
                  : 'border-ink-200 dark:border-ink-700 hover:border-ink-400'
              }`}
            >
              <div
                className="absolute inset-1 rounded-full"
                style={{
                  background: p.colorHex,
                  boxShadow: p.color === 'Rose' ? 'inset 0 0 0 1px rgba(0,0,0,0.08)' : 'none',
                }}
              />
              {selectedColor === p.color && (
                <div className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-volt-500 flex items-center justify-center">
                  <Check size={12} className="text-white" />
                </div>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Quantity selector */}
      <div className="flex items-center gap-4">
        <span className="text-sm text-ink-600 dark:text-ink-300">Quantité :</span>
        <div className="flex items-center border border-ink-200 dark:border-ink-700 rounded-full">
          <button
            onClick={() => setQuantity(Math.max(1, quantity - 1))}
            className="w-10 h-10 flex items-center justify-center hover:bg-ink-100 dark:hover:bg-ink-800 rounded-full transition-colors"
            aria-label="Diminuer"
          >
            <Minus size={14} />
          </button>
          <span className="w-10 text-center text-sm font-medium tabular-nums">
            {quantity}
          </span>
          <button
            onClick={() => setQuantity(quantity + 1)}
            className="w-10 h-10 flex items-center justify-center hover:bg-ink-100 dark:hover:bg-ink-800 rounded-full transition-colors"
            aria-label="Augmenter"
          >
            <Plus size={14} />
          </button>
        </div>
      </div>

      {/* Add to cart */}
      <button
        onClick={handleAdd}
        className={`btn-primary w-full transition-all ${
          added ? '!bg-success !text-white' : ''
        }`}
      >
        {added ? (
          <>
            <Check size={16} />
            Ajouté au panier
          </>
        ) : (
          <>
            Ajouter au panier
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" aria-hidden="true">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </>
        )}
      </button>
    </div>
  );
}
