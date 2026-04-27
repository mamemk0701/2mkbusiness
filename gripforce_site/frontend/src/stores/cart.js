import { persistentAtom } from '@nanostores/persistent';
import { computed } from 'nanostores';

// Structure d'un item du panier
// { id: 'gripforce-noir', name: 'GripForce Noir', color: 'Noir', price: 4500, quantity: 1, image: '/products/gripforce-noir.webp' }

export const $cart = persistentAtom('gripforce_cart', [], {
  encode: JSON.stringify,
  decode: JSON.parse,
});

export const $cartCount = computed($cart, (cart) =>
  cart.reduce((sum, item) => sum + item.quantity, 0)
);

export const $cartTotal = computed($cart, (cart) =>
  cart.reduce((sum, item) => sum + item.price * item.quantity, 0)
);

export function addToCart(product) {
  const cart = $cart.get();
  const existing = cart.find((item) => item.id === product.id);

  if (existing) {
    $cart.set(
      cart.map((item) =>
        item.id === product.id
          ? { ...item, quantity: item.quantity + (product.quantity || 1) }
          : item
      )
    );
  } else {
    $cart.set([...cart, { ...product, quantity: product.quantity || 1 }]);
  }
}

export function removeFromCart(id) {
  $cart.set($cart.get().filter((item) => item.id !== id));
}

export function updateQuantity(id, quantity) {
  if (quantity <= 0) {
    removeFromCart(id);
    return;
  }
  $cart.set(
    $cart.get().map((item) =>
      item.id === id ? { ...item, quantity } : item
    )
  );
}

export function clearCart() {
  $cart.set([]);
}
