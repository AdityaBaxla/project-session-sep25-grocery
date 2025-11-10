import { defineStore } from "pinia";

export const useCartStore = defineStore("cart", {
  state: () => ({
    items: (() => {
      try {
        const saved = localStorage.getItem("cart");
        return saved ? JSON.parse(saved) : [];
      } catch (e) {
        console.warn("Failed to parse cart from localStorage", e);
        return [];
      }
    })(),
  }),

  getters: {
    count: (state) =>
      state.items.reduce((sum, item) => sum + (item.qty || 0), 0),

    total: (state) =>
      state.items.reduce((sum, item) => sum + item.price * item.qty, 0),

    isEmpty: (state) => state.items.length === 0,
  },

  actions: {
    addItem(product, quantity = 1) {
      const existing = this.items.find((i) => i.id === product.id);

      if (existing) {
        existing.qty += quantity;
      } else {
        this.items.push({
          id: product.id,
          name: product.name,
          price: product.price,
          image: product.image,
          qty: quantity,
        });
      }

      this.saveToStorage();
    },

    updateQuantity(productId, quantity) {
      const item = this.items.find((i) => i.id === productId);
      if (item) {
        item.qty = Math.max(0, quantity);
        if (item.qty === 0) {
          this.removeItem(productId);
        } else {
          this.saveToStorage();
        }
      }
    },

    removeItem(productId) {
      const index = this.items.findIndex((i) => i.id === productId);
      if (index > -1) {
        this.items.splice(index, 1);
        this.saveToStorage();
      }
    },

    clearCart() {
      this.items = [];
      this.saveToStorage();
    },

    saveToStorage() {
      localStorage.setItem("cart", JSON.stringify(this.items));
    },
  },
});
