<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
    <div class="container">
      <router-link class="navbar-brand fw-bold" to="/">GroceryApp</router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#mainNav"
        aria-controls="mainNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="mainNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item" v-if="isAuthenticated">
            <router-link class="nav-link" to="/products">Products</router-link>
          </li>
          <li class="nav-item" v-if="isManager">
            <router-link class="nav-link" to="/manager/sections"
              >Edit Sections</router-link
            >
          </li>
          <li class="nav-item" v-if="isManager">
            <router-link class="nav-link" to="/manager/products"
              >Edit Products</router-link
            >
          </li>

          <li class="nav-item" v-if="isAuthenticated">
            <router-link class="nav-link" to="/orders">My Orders</router-link>
          </li>

          <li class="nav-item" v-if="isAdmin">
            <router-link class="nav-link text-warning" to="/admin"
              >Admin</router-link
            >
          </li>
        </ul>

        <ul class="navbar-nav ms-auto mb-2 mb-lg-0 align-items-center">
          <!-- Cart Dropdown -->
          <li class="nav-item dropdown me-2" v-if="isCustomer">
            <a
              class="nav-link position-relative"
              href="#"
              id="cartMenu"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <i class="bi bi-cart3 fs-5"></i>
              <span
                v-if="cartItemsCount"
                class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                style="font-size: 0.65rem"
              >
                {{ cartItemsCount }}
              </span>
            </a>

            <div
              class="dropdown-menu dropdown-menu-end p-3"
              aria-labelledby="cartMenu"
              style="min-width: 320px; max-height: 480px; overflow-y: auto"
            >
              <h6 class="dropdown-header border-bottom pb-2 mb-2">
                Shopping Cart
              </h6>

              <div v-if="cartStore.isEmpty" class="text-center text-muted py-3">
                Your cart is empty
              </div>

              <template v-else>
                <div
                  v-for="item in cartStore.items"
                  :key="item.id"
                  class="d-flex align-items-center gap-2 mb-2"
                >
                  <img
                    :src="item.image"
                    class="rounded"
                    style="width: 48px; height: 48px; object-fit: cover"
                    :alt="item.name"
                  />
                  <div class="flex-grow-1">
                    <div class="fw-medium">{{ item.name }}</div>
                    <div class="text-muted small">
                      {{ formatPrice(item.price) }} × {{ item.qty }}
                    </div>
                  </div>
                  <button
                    @click="removeFromCart(item.id)"
                    class="btn btn-sm btn-link text-danger p-1"
                    title="Remove item"
                  >
                    <i class="bi bi-x-lg"></i>
                  </button>
                </div>

                <div class="border-top mt-3 pt-3">
                  <div
                    class="d-flex justify-content-between align-items-center mb-3"
                  >
                    <span class="text-muted"
                      >Total ({{ cartItemsCount }} items)</span
                    >
                    <span class="fw-bold">{{
                      formatPrice(cartStore.total)
                    }}</span>
                  </div>
                  <div class="d-grid">
                    <button @click="checkout" class="btn btn-primary">
                      Checkout Now
                    </button>
                  </div>
                </div>
              </template>
            </div>
          </li>

          <template v-if="!userStore.isAuthenticated">
            <li class="nav-item me-2">
              <router-link class="btn btn-outline-primary btn-sm" to="/login"
                >Login</router-link
              >
            </li>
            <li class="nav-item">
              <router-link class="btn btn-primary btn-sm" to="/signup"
                >Sign up</router-link
              >
            </li>
          </template>

          <template v-else>
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle d-flex align-items-center"
                href="#"
                id="accountMenu"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <span
                  class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center me-2"
                  :style="{ width: '36px', height: '36px', fontSize: '0.9rem' }"
                >
                  {{ userInitial }}
                </span>
                <span class="small">{{ displayName }}</span>
              </a>
              <ul
                class="dropdown-menu dropdown-menu-end"
                aria-labelledby="accountMenu"
              >
                <li>
                  <router-link class="dropdown-item" to="/profile"
                    >Profile</router-link
                  >
                </li>
                <li>
                  <router-link class="dropdown-item" to="/settings"
                    >Settings</router-link
                  >
                </li>
                <li><hr class="dropdown-divider" /></li>
                <li>
                  <button
                    class="dropdown-item text-danger"
                    @click.prevent="handleLogout"
                  >
                    Logout
                  </button>
                </li>
              </ul>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { useUserStore } from "@/stores/user";
import { useCartStore } from "@/stores/cart";

export default {
  name: "Navbar",
  data() {
    return {
      userStore: null,
      cartStore: null,
    };
  },
  created() {
    // attach Pinia store so template reacts to changes
    this.userStore = useUserStore();
    this.cartStore = useCartStore();
  },
  computed: {
    isAuthenticated() {
      return this.userStore && this.userStore.isAuthenticated;
    },
    isAdmin() {
      return this.userStore && this.userStore.isAdmin;
    },
    isCustomer() {
      return this.userStore?.user?.role === "customer";
    },
    isManager() {
      return this.userStore?.user?.role === "manager";
    },
    displayName() {
      if (!this.userStore || !this.userStore.user) return "Account";
      return this.userStore.user.name || this.userStore.user.email || "Account";
    },
    userInitial() {
      const name =
        this.userStore &&
        this.userStore.user &&
        (this.userStore.user.name || this.userStore.user.email);
      return name ? String(name).charAt(0).toUpperCase() : "U";
    },
    cartItemsCount() {
      return this.cartStore?.count || 0;
    },
  },
  methods: {
    handleLogout() {
      if (this.userStore) {
        this.userStore.logout();
      }
      this.$router.push("/login");
    },
    formatPrice(val) {
      if (val == null || isNaN(Number(val))) return "-";
      return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
      }).format(Number(val));
    },
    removeFromCart(productId) {
      this.cartStore.removeItem(productId);
    },
    checkout() {
      if (this.cartStore.isEmpty) return;
      this.$router.push("/checkout");
    },
  },
};
</script>

<style scoped>
.navbar-brand {
  letter-spacing: 0.3px;
}
.rounded-circle {
  flex: 0 0 auto;
}
.dropdown-toggle::after {
  margin-left: 0.45rem;
}
.dropdown-menu {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}
.badge {
  font-size: 0.65rem;
  min-width: 1.5em;
}
</style>
