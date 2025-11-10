<template>
  <div>
    <!-- Hero Section -->
    <div class="bg-primary bg-gradient text-white py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6">
            <h1 class="display-4 fw-bold mb-3">
              Fresh Groceries Delivered to Your Door
            </h1>
            <p class="lead mb-4">
              Shop from our wide selection of fresh produce, pantry essentials,
              and household items.
            </p>
            <router-link to="/products" class="btn btn-light btn-lg">
              Start Shopping
            </router-link>
          </div>
          <div class="col-lg-6 d-none d-lg-block text-center">
            <!-- Replaced image with Bootstrap icon -->
            <i
              class="bi bi-basket2-fill display-1 mb-3"
              style="font-size: 200px"
            ></i>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="container py-5">
      <div class="row g-4">
        <div class="col-md-4">
          <div class="card h-100 border-0 shadow-sm">
            <div class="card-body text-center p-4">
              <div class="display-5 mb-3 text-primary">
                <i class="bi bi-truck"></i>
              </div>
              <h5 class="card-title">Fast Delivery</h5>
              <p class="card-text text-muted">
                Same-day delivery available for orders placed before 2 PM
              </p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card h-100 border-0 shadow-sm">
            <div class="card-body text-center p-4">
              <div class="display-5 mb-3 text-primary">
                <i class="bi bi-bag-heart"></i>
              </div>
              <h5 class="card-title">Fresh Products</h5>
              <p class="card-text text-muted">
                Handpicked fresh items from trusted local suppliers
              </p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card h-100 border-0 shadow-sm">
            <div class="card-body text-center p-4">
              <div class="display-5 mb-3 text-primary">
                <i class="bi bi-shield-check"></i>
              </div>
              <h5 class="card-title">Secure Checkout</h5>
              <p class="card-text text-muted">
                Safe and secure payment options for worry-free shopping
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Categories Section -->
    <div class="bg-light py-5">
      <div class="container">
        <h2 class="text-center mb-4">Popular Categories</h2>
        <div class="row g-4">
          <div
            v-for="category in categories"
            :key="category.name"
            class="col-6 col-md-3"
          >
            <router-link
              :to="{ path: '/products', query: { category: category.name } }"
              class="text-decoration-none"
            >
              <div class="card h-100 border-0 shadow-sm hover-lift">
                <div class="card-body text-center p-4">
                  <i
                    :class="category.icon + ' display-6 mb-3 text-primary'"
                  ></i>
                  <h6 class="card-title text-dark">{{ category.name }}</h6>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      categories: [
        { name: "Fruits & Vegetables", icon: "bi bi-apple" },
        { name: "Dairy & Eggs", icon: "bi bi-egg-fried" },
        { name: "Bakery", icon: "bi bi-bread-slice" },
        { name: "Beverages", icon: "bi bi-cup-straw" },
        { name: "Snacks", icon: "bi bi-cookie" },
        { name: "Household", icon: "bi bi-house-heart" },
        { name: "Personal Care", icon: "bi bi-moisture" },
        { name: "Frozen Foods", icon: "bi bi-snow2" },
      ],
    };
  },
};
</script>

<style scoped>
.hover-lift {
  transition: transform 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-5px);
}
.bg-primary {
  background: linear-gradient(45deg, #0d6efd, #0dcaf0) !important;
}
.bi-basket2-fill {
  opacity: 0.9;
  opacity: 0.9;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1) 2px 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
