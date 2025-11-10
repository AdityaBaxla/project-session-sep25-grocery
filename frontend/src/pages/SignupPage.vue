<template>
  <div class="container py-5" style="max-width: 720px">
    <div class="card shadow-sm">
      <div class="card-body">
        <h3 class="card-title mb-3 text-center">Create account</h3>

        <ul class="nav nav-pills mb-4 justify-content-center" role="tablist">
          <li class="nav-item" role="presentation">
            <button
              class="nav-link"
              :class="{ active: role === 'customer' }"
              @click="role = 'customer'"
              type="button"
            >
              Customer
            </button>
          </li>
          <li class="nav-item ms-2" role="presentation">
            <button
              class="nav-link"
              :class="{ active: role === 'manager' }"
              @click="role = 'manager'"
              type="button"
            >
              Manager
            </button>
          </li>
        </ul>

        <form @submit.prevent="submitSignup" novalidate>
          <div class="row g-3">
            <div class="col-12 col-md-6">
              <label class="form-label" for="name">Full name</label>
              <input
                id="name"
                v-model="name"
                type="text"
                class="form-control"
                placeholder="Jane Doe"
                required
              />
            </div>

            <div class="col-12 col-md-6">
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

            <div class="col-12 col-md-6">
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

            <div class="col-12 col-md-6">
              <label class="form-label" for="confirmPassword"
                >Confirm password</label
              >
              <input
                id="confirmPassword"
                v-model="confirmPassword"
                type="password"
                class="form-control"
                placeholder="••••••••"
                required
              />
            </div>

            <!-- Manager specific fields -->
            <template v-if="role === 'manager'">
              <div class="col-12">
                <label class="form-label" for="department">Department</label>
                <input
                  id="department"
                  v-model="department"
                  type="text"
                  class="form-control"
                  placeholder="e.g. Produce"
                />
              </div>

              <div class="col-12 col-md-6">
                <label class="form-label" for="salary">Salary (annual)</label>
                <input
                  id="salary"
                  v-model.number="salary"
                  type="number"
                  class="form-control"
                  min="0"
                  placeholder="30000"
                />
              </div>

              <div class="col-12 col-md-6">
                <label class="form-label" for="address">Address</label>
                <input
                  id="address"
                  v-model="address"
                  type="text"
                  class="form-control"
                  placeholder="Street, City"
                />
              </div>
            </template>

            <div class="col-12">
              <div v-if="error" class="text-danger mb-2 small">{{ error }}</div>
            </div>

            <div class="col-12 d-grid">
              <button
                class="btn btn-primary btn-lg"
                :disabled="loading"
                type="submit"
              >
                <span
                  v-if="loading"
                  class="spinner-border spinner-border-sm me-2"
                  role="status"
                  aria-hidden="true"
                ></span>
                {{ loading ? "Creating account…" : "Sign up" }}
              </button>
            </div>

            <div class="col-12 text-center">
              <small class="text-muted">
                Already have an account?
                <router-link to="/login">Login</router-link>
              </small>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/utils/api";
import { useUserStore } from "@/stores/user";

export default {
  name: "SignupPage",
  data() {
    return {
      role: "customer", // "customer" or "manager"
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
      // manager fields
      department: "",
      salary: null,
      address: "",
      loading: false,
      error: "",
      userStore: null,
    };
  },
  created() {
    this.userStore = useUserStore();
  },
  methods: {
    async submitSignup() {
      this.error = "";
      if (this.password !== this.confirmPassword) {
        this.error = "Passwords do not match";
        return;
      }

      this.loading = true;
      try {
        // Build payload according to selected role
        const payload = {
          name: this.name,
          email: this.email,
          password: this.password,
          role: this.role, // backend can map this to roles
        };

        if (this.role === "manager") {
          payload.manager = {
            department: this.department || null,
            salary: this.salary != null ? Number(this.salary) : null,
            address: this.address || null,
          };
        }

        // Call signup endpoint (adjust path if your backend uses different URL)
        const res = await api.post("/auth/register", payload);
        // Redirect to login
        alert("Signup successful! Please login.");
        this.$router.push("/login");
      } catch (err) {
        this.error =
          (err && err.message) ||
          (err && err.message) ||
          "Signup failed. Please try again.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.card {
  border-radius: 12px;
}
.nav-pills .nav-link {
  border-radius: 999px;
  padding: 0.6rem 1.1rem;
}
.nav-pills .nav-link.active {
  background: linear-gradient(90deg, #3d3e40, #3d3e40);
  color: #fff;
  box-shadow: 0 4px 14px rgba(78, 70, 228, 0.12);
}
input::placeholder {
  color: #adb5bd;
}
</style>
