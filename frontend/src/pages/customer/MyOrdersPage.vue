<template>
  <div class="container py-4">
    <h4 class="mb-4">My Orders</h4>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div
      v-if="!loading && orders.length === 0"
      class="text-center text-muted py-5"
    >
      You have no orders yet.
      <router-link to="/products">Start shopping</router-link>.
    </div>

    <div class="accordion" id="ordersAccordion" v-if="orders.length">
      <div
        v-for="order in orders"
        :key="order.id"
        class="accordion-item mb-3 shadow-sm"
      >
        <h2 class="accordion-header" :id="'heading' + order.id">
          <button
            class="accordion-button collapsed d-flex justify-content-between align-items-center"
            type="button"
            data-bs-toggle="collapse"
            :data-bs-target="'#collapse' + order.id"
            aria-expanded="false"
            :aria-controls="'collapse' + order.id"
          >
            <div class="me-3">
              <div class="small text-muted">Order #{{ order.id }}</div>
              <div class="fw-semibold">{{ formatDate(order.created_at) }}</div>
            </div>

            <div class="ms-auto text-end">
              <div class="fw-bold">
                {{ formatPrice(order.total_amount || order.total) }}
              </div>
            </div>
          </button>
        </h2>

        <div
          :id="'collapse' + order.id"
          class="accordion-collapse collapse"
          :aria-labelledby="'heading' + order.id"
          data-bs-parent="#ordersAccordion"
        >
          <div class="accordion-body">
            <div
              v-if="!order.items || order.items.length === 0"
              class="text-muted small"
            >
              No items found for this order.
            </div>

            <div v-else>
              <div class="list-group mb-3">
                <div
                  class="list-group-item d-flex align-items-center"
                  v-for="item in order.items"
                  :key="item.id"
                >
                  <img
                    :src="
                      (item.product && item.product.image) || placeholderSrc
                    "
                    alt="item"
                    class="rounded"
                    style="
                      width: 64px;
                      height: 64px;
                      object-fit: cover;
                      margin-right: 12px;
                    "
                  />
                  <div class="flex-grow-1">
                    <div class="fw-semibold">
                      {{
                        (item.product && item.product.name) ||
                        item.name ||
                        "Product"
                      }}
                    </div>
                    <div class="small text-muted">
                      {{ item.quantity }} ×
                      {{ formatPrice(item.price_at_sale || item.price) }}
                    </div>
                  </div>
                  <div class="text-end fw-semibold">
                    {{
                      formatPrice(
                        (item.price_at_sale || item.price) *
                          (item.quantity || 1)
                      )
                    }}
                  </div>
                </div>
              </div>

              <div class="d-flex justify-content-between align-items-center">
                <div class="small text-muted">
                  Payment:
                  <span class="fw-medium">{{
                    order.payment_method || "N/A"
                  }}</span>
                </div>
                <div class="fw-bold">
                  Total: {{ formatPrice(order.total_amount || order.total) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/utils/api";

export default {
  name: "MyOrdersPage",
  data() {
    return {
      orders: [],
      loading: false,
      error: "",
      placeholderSrc: "/placeholder.svg",
    };
  },
  created() {
    this.fetchOrders();
  },
  methods: {
    async fetchOrders() {
      this.loading = true;
      this.error = "";
      try {
        const res = await api.get("/orders");
        const payload = Array.isArray(res) ? res : res.data || res.orders || [];

        this.orders = (payload || [])
          .map((o) => {
            // prefer backend key 'sale_items' (or common variants), fallback to 'items'
            const rawItems =
              o.sale_items || o.saleItems || o.saleItems || o.items || [];

            return {
              ...o,
              items: (rawItems || []).map((it) => ({
                id: it.id,
                quantity: Number(it.quantity || it.qty || 0),
                price_at_sale: Number(
                  it.price_at_sale || it.price || it.unit_price || 0
                ),
                product:
                  it.product ||
                  (it.product_id
                    ? {
                        id: it.product_id,
                        name: it.product_name || it.name,
                        image: it.image,
                      }
                    : null),
                ...it,
              })),
              total_amount: Number(
                o.total_amount || o.total || o.totalAmount || 0
              ),
            };
          })
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      } catch (err) {
        this.error = (err && err.message) || "Failed to load orders";
      } finally {
        this.loading = false;
      }
    },

    formatPrice(val) {
      if (val == null || isNaN(Number(val))) return "-";
      return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 2,
      }).format(Number(val));
    },
    formatDate(dt) {
      if (!dt) return "";
      try {
        return new Date(dt).toLocaleString();
      } catch {
        return String(dt);
      }
    },
    statusClass(status) {
      const s = (status || "").toLowerCase();
      if (s.includes("pending")) return "bg-warning text-dark";
      if (s.includes("cancel")) return "bg-danger text-white";
      if (s.includes("completed") || s.includes("delivered"))
        return "bg-success text-white";
      return "bg-secondary text-white";
    },
  },
};
</script>

<style scoped>
.accordion-button {
  gap: 1rem;
}
.badge {
  font-size: 0.75rem;
  padding: 0.35em 0.6em;
  border-radius: 0.375rem;
}
</style>
