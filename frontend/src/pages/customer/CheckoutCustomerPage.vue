<template>
  <div class="container py-4">
    <h4 class="mb-4">Checkout</h4>

    <div class="row g-4">
      <!-- Cart Items -->
      <div class="col-lg-8">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title mb-4">Order Summary</h5>

            <div v-if="cartStore.isEmpty" class="text-center py-4 text-muted">
              Your cart is empty.
              <router-link to="/products">Continue shopping</router-link>
            </div>

            <template v-else>
              <!-- Cart Items List -->
              <div class="mb-3" v-for="item in cartStore.items" :key="item.id">
                <div class="d-flex gap-3 p-2 border rounded">
                  <img
                    :src="item.image"
                    class="rounded"
                    style="width: 80px; height: 80px; object-fit: cover"
                    :alt="item.name"
                  />
                  <div class="flex-grow-1">
                    <h6 class="mb-1">{{ item.name }}</h6>
                    <div class="text-muted small mb-2">
                      {{ formatPrice(item.price) }} × {{ item.qty }}
                    </div>
                    <div class="d-flex align-items-center gap-2">
                      <div
                        class="input-group input-group-sm"
                        style="width: 100px"
                      >
                        <button
                          class="btn btn-outline-secondary"
                          @click="updateQuantity(item.id, item.qty - 1)"
                          :disabled="item.qty <= 1"
                        >
                          -
                        </button>
                        <input
                          type="number"
                          class="form-control text-center"
                          v-model.number="item.qty"
                          min="1"
                        />
                        <button
                          class="btn btn-outline-secondary"
                          @click="updateQuantity(item.id, item.qty + 1)"
                        >
                          +
                        </button>
                      </div>
                      <button
                        @click="removeItem(item.id)"
                        class="btn btn-sm btn-link text-danger"
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                  <div class="text-end">
                    <div class="fw-bold">
                      {{ formatPrice(item.price * item.qty) }}
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Order Summary -->
      <div class="col-lg-4">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title mb-4">Payment Details</h5>

            <div class="mb-4">
              <div class="d-flex justify-content-between mb-2">
                <span class="text-muted">Subtotal</span>
                <span>{{ formatPrice(cartStore.total) }}</span>
              </div>
              <div class="d-flex justify-content-between mb-2">
                <span class="text-muted">Shipping</span>
                <span>{{ formatPrice(shippingCost) }}</span>
              </div>
              <div class="d-flex justify-content-between fw-bold">
                <span>Total</span>
                <span>{{ formatPrice(cartStore.total + shippingCost) }}</span>
              </div>
            </div>

            <form @submit.prevent="handleCheckout">
              <div class="mb-3">
                <label class="form-label">Delivery Address</label>
                <textarea
                  v-model="address"
                  class="form-control"
                  rows="3"
                  required
                ></textarea>
              </div>

              <div class="mb-3">
                <label class="form-label">Phone Number</label>
                <input
                  type="tel"
                  v-model="phone"
                  class="form-control"
                  required
                />
              </div>

              <button
                type="submit"
                class="btn btn-primary w-100"
                :disabled="loading || cartStore.isEmpty"
              >
                <span
                  v-if="loading"
                  class="spinner-border spinner-border-sm me-2"
                ></span>
                {{ loading ? "Processing..." : "Place Order" }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useCartStore } from "@/stores/cart";
import api from "@/utils/api";

export default {
  name: "CheckoutCustomerPage",
  data() {
    return {
      cartStore: null,
      loading: false,
      error: null,
      address: "",
      phone: "",
      shippingCost: 50, // Fixed shipping cost (can be made dynamic)
    };
  },
  created() {
    this.cartStore = useCartStore();
    // Redirect if cart is empty
    if (this.cartStore.isEmpty) {
      this.$router.push("/products");
    }
  },
  methods: {
    formatPrice(val) {
      if (val == null || isNaN(Number(val))) return "-";
      return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 2,
      }).format(Number(val));
    },
    updateQuantity(productId, qty) {
      if (qty < 1) return;
      this.cartStore.updateQuantity(productId, qty);
    },
    removeItem(productId) {
      this.cartStore.removeItem(productId);
      if (this.cartStore.isEmpty) {
        this.$router.push("/products");
      }
    },
    async handleCheckout() {
      if (this.loading || this.cartStore.isEmpty) return;

      this.loading = true;
      this.error = null;

      try {
        // Format items as expected by the /purchase/items endpoint
        const items = this.cartStore.items.map((item) => ({
          product_id: item.id,
          quantity: item.qty,
        }));

        // Call purchase endpoint
        const response = await api.post("/purchase/items", { items });

        // Clear cart after successful order
        this.cartStore.clearCart();

        // Save order details for confirmation page
        localStorage.setItem(
          "lastOrder",
          JSON.stringify({
            total: response.total,
            orderId: response.sale_id,
            address: this.address,
            phone: this.phone,
          })
        );

        // Redirect to order confirmation
        this.$router.push({
          path: "/order-confirmation",
          query: {
            order_id: response.sale_id,
            success: true,
          },
        });
      } catch (err) {
        this.error = err.message || "Failed to place order";
        alert(this.error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.card img {
  object-fit: cover;
}
.input-group .input-group-text {
  border-right: 0;
}
.input-group input.form-control {
  border-left: 0;
}
.ratio img {
  width: 100%;
  height: 100%;
}
.position-fixed.top-0 {
  top: 1rem;
}
</style>
