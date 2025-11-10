<template>
  <div class="container py-5" style="max-width: 420px">
    <div class="card shadow-sm">
      <div class="card-body">
        <h3 class="card-title mb-3 text-center">Sign in</h3>

        <form @submit.prevent="submitLogin" novalidate>
          <div class="mb-3">
            <label class="form-label" for="email">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              class="form-control"
              placeholder="you@example.com"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label" for="password">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              class="form-control"
              placeholder="••••••••"
              required
            />
          </div>

          <div v-if="error" class="text-danger mb-2 small">{{ error }}</div>

          <button
            type="submit"
            class="btn btn-primary w-100"
            :disabled="loading"
          >
            <span
              v-if="loading"
              class="spinner-border spinner-border-sm me-2"
              role="status"
              aria-hidden="true"
            ></span>
            {{ loading ? "Signing in…" : "Login" }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "@/stores/user";

export default {
  name: "LoginPage",
  data() {
    return {
      email: "",
      password: "",
      loading: false,
      error: "",
      userStore: null,
    };
  },
  created() {
    this.userStore = useUserStore();
  },
  methods: {
    async submitLogin() {
      this.error = "";
      this.loading = true;
      try {
        // call with endpoint then credentials (store expects (endpoint, credentials))
        await this.userStore.loginWithCredentials("/auth/login", {
          email: this.email,
          password: this.password,
        });
        this.$router.push("/products");
      } catch (e) {
        this.error = e.message || "Login failed";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
<style scoped>
/* tiny visual polish */
.card {
  border-radius: 12px;
}
</style>
