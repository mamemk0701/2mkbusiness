import { useStore } from '@nanostores/react';
import { ShoppingBag } from 'lucide-react';
import { $cartCount } from '../stores/cart.js';

export default function CartButton() {
  const count = useStore($cartCount);

  const openDrawer = () => {
    window.dispatchEvent(new CustomEvent('cart:open'));
  };

  return (
    <button
      onClick={openDrawer}
      aria-label={`Panier (${count} article${count > 1 ? 's' : ''})`}
      className="relative w-9 h-9 md:w-10 md:h-10 rounded-full border border-ink-200 dark:border-ink-700 hover:border-ink-400 dark:hover:border-ink-500 transition-colors flex items-center justify-center"
    >
      <ShoppingBag size={16} />
      {count > 0 && (
        <span className="absolute -top-1 -right-1 w-4.5 h-4.5 min-w-[18px] h-[18px] px-1 bg-volt-500 text-white text-[10px] font-semibold rounded-full flex items-center justify-center">
          {count}
        </span>
      )}
    </button>
  );
}
