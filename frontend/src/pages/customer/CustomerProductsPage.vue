<template>
  <div class="container py-4">
    <!-- transient alert -->
    <div
      v-if="showAlert"
      class="alert alert-success position-fixed end-0 top-0 m-3"
      role="alert"
      style="z-index: 1050"
    >
      {{ cartAlert }}
    </div>

    <div class="d-flex flex-column flex-md-row align-items-start gap-3 mb-4">
      <div class="flex-fill">
        <div class="input-group">
          <span class="input-group-text bg-white"
            ><i class="bi bi-search"></i
          ></span>
          <input
            v-model="search"
            @input="onSearchInput"
            type="search"
            class="form-control"
            placeholder="Search products by name or description..."
            aria-label="Search products"
          />
        </div>
      </div>

      <div style="min-width: 200px">
        <select v-model="selectedCategory" class="form-select">
          <option value="">All categories</option>
          <option v-for="cat in categories" :key="cat" :value="cat">
            {{ cat }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-if="error" class="alert alert-danger small">{{ error }}</div>

    <div
      v-if="!loading && filteredProducts.length === 0"
      class="text-center text-muted py-5"
    >
      No products found.
    </div>

    <div class="row g-3">
      <div
        v-for="product in filteredProducts"
        :key="product.id"
        class="col-12 col-sm-6 col-md-4 col-lg-3"
      >
        <div class="card h-100 shadow-sm">
          <div class="ratio ratio-4x3">
            <component
              :is="product.image ? 'img' : 'PlaceholderImage'"
              v-if="!product.image"
              class="card-img-top object-fit-cover"
              :src="product.image"
              :alt="product.name || 'Product image'"
            />
            <img
              v-else
              :src="product.image"
              class="card-img-top object-fit-cover"
              :alt="product.name || 'Product image'"
            />
          </div>

          <div class="card-body d-flex flex-column">
            <h6 class="card-title mb-1">{{ product.name }}</h6>
            <p class="text-muted small mb-2" v-if="product.description">
              {{ truncate(product.description, 80) }}
            </p>

            <div class="mt-auto d-flex flex-column gap-2">
              <div class="d-flex justify-content-between align-items-center">
                <div>
                  <div class="fw-bold text-primary">
                    {{ formatPrice(product.price) }}
                  </div>
                  <div class="small text-muted">
                    {{ product.category || product.section || "Uncategorized" }}
                  </div>
                </div>

                <div class="text-end">
                  <div
                    v-if="product.stock != null"
                    :class="
                      product.stock > 0
                        ? 'text-success small'
                        : 'text-danger small'
                    "
                  >
                    {{ product.stock > 0 ? "In stock" : "Out of stock" }}
                  </div>
                </div>
              </div>

              <div class="d-flex gap-2 align-items-center">
                <div class="input-group input-group-sm" style="width: 120px">
                  <button
                    class="btn btn-outline-secondary"
                    type="button"
                    @click="decreaseQty(product.id)"
                    :disabled="quantities[product.id] <= 1"
                  >
                    -
                  </button>
                  <input
                    type="number"
                    class="form-control text-center"
                    v-model.number="quantities[product.id]"
                    :min="1"
                    :max="product.stock != null ? product.stock : null"
                  />
                  <button
                    class="btn btn-outline-secondary"
                    type="button"
                    @click="increaseQty(product.id, product.stock)"
                    :disabled="product.stock === 0"
                  >
                    +
                  </button>
                </div>

                <button
                  class="btn btn-sm btn-primary ms-auto"
                  :disabled="product.stock === 0"
                  @click="addToCart(product)"
                >
                  <i class="bi bi-cart-plus me-1"></i> Add to cart
                </button>
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
import PlaceholderImage from "@/components/PlaceholderImage.vue";
import { useCartStore } from "@/stores/cart";

export default {
  name: "ProductsPage",
  components: {
    PlaceholderImage,
  },
  data() {
    return {
      products: [],
      categories: [],
      selectedCategory: "",
      search: "",
      loading: false,
      error: "",
      searchTimeout: null,
      quantities: {}, // per-product selected quantity
      showAlert: false,
      cartAlert: "",
      cartStore: null,
    };
  },
  computed: {
    filteredProducts() {
      const q = this.search && String(this.search).trim().toLowerCase();
      return this.products.filter((p) => {
        if (
          this.selectedCategory &&
          String(p.category || p.section || "").toLowerCase() !==
            String(this.selectedCategory).toLowerCase()
        ) {
          return false;
        }
        if (!q) return true;
        const name = String(p.name || "").toLowerCase();
        const desc = String(p.description || "").toLowerCase();
        return name.includes(q) || desc.includes(q);
      });
    },
  },
  created() {
    this.cartStore = useCartStore();
    this.fetchProducts();
    this.fetchCategories();
  },
  methods: {
    async fetchProducts() {
      this.loading = true;
      this.error = "";
      try {
        const res = await api.get("/products");
        this.products = (res && (res.data || res)) || [];
        this.products = this.products.map((p) => ({
          id: p.id || p._id || null,
          name: p.name || p.title || "Product",
          description: p.description || p.desc || "",
          price: p.price != null ? p.price : p.cost || 0,
          image: p.image || p.img || p.photo || null,
          category:
            p.category || (p.section && p.section.name) || p.section || null,
          stock:
            p.stock != null ? p.stock : p.quantity != null ? p.quantity : null,
          ...p,
        }));

        // initialize quantities map (default 1)
        this.products.forEach((p) => {
          const id = p.id || JSON.stringify(p);
          this.$set
            ? this.$set(this.quantities, id, 1)
            : (this.quantities[id] = 1);
        });
      } catch (err) {
        this.error = (err && err.message) || "Failed to load products";
      } finally {
        this.loading = false;
      }
    },
    async fetchCategories() {
      try {
        const res = await api.get("/sections");
        let cats = (res && (res.data || res)) || [];
        if (!Array.isArray(cats) || cats.length === 0) {
          cats = Array.from(
            new Set(
              (this.products || []).map((p) => p.category).filter(Boolean)
            )
          );
        }
        this.categories = cats
          .map((c) =>
            typeof c === "string" ? c : c.name || c.title || String(c)
          )
          .filter(Boolean);
      } catch {
        this.categories = Array.from(
          new Set((this.products || []).map((p) => p.category).filter(Boolean))
        );
      }
    },
    truncate(str, n) {
      if (!str) return "";
      return str.length > n ? str.slice(0, n - 1) + "…" : str;
    },
    formatPrice(val) {
      if (val == null || isNaN(Number(val))) return "-";
      return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 2,
      }).format(Number(val));
    },
    onSearchInput() {
      clearTimeout(this.searchTimeout); // debounce
      this.searchTimeout = setTimeout(() => {
        // computed updates automatically
      }, 2000);
    },
    increaseQty(productId, stock) {
      const current = Number(this.quantities[productId] || 1);
      if (stock != null && current >= stock) return;
      this.$set
        ? this.$set(this.quantities, productId, current + 1)
        : (this.quantities[productId] = current + 1);
    },
    decreaseQty(productId) {
      const current = Number(this.quantities[productId] || 1);
      if (current <= 1) return;
      this.$set
        ? this.$set(this.quantities, productId, current - 1)
        : (this.quantities[productId] = current - 1);
    },
    addToCart(product) {
      const id = product.id || JSON.stringify(product);
      const qty = Math.max(1, Number(this.quantities[id] || 1));

      if (product.stock != null && qty > product.stock) {
        this.cartAlert = `Only ${product.stock} units available for "${product.name}".`;
        this.showTransientAlert();
        return;
      }

      try {
        this.cartStore.addItem(product, qty);
        this.cartAlert = `Added ${qty} × "${product.name}" to cart.`;
        this.showTransientAlert();

        // Reset quantity after adding to cart
        this.$set
          ? this.$set(this.quantities, id, 1)
          : (this.quantities[id] = 1);
      } catch (error) {
        this.cartAlert = "Failed to add item to cart.";
        this.showTransientAlert();
      }
    },
    showTransientAlert(timeout = 2500) {
      this.showAlert = true;
      clearTimeout(this._alertTimer);
      this._alertTimer = setTimeout(() => {
        this.showAlert = false;
      }, timeout);
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
