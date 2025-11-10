<template>
  <div class="container py-4">
    <h4 class="mb-4">Manage Products (requests)</h4>

    <div class="card mb-3 p-3">
      <form @submit.prevent="submitRequest">
        <div class="row g-2">
          <div class="col-md-4">
            <label class="form-label small">Name</label>
            <input v-model="form.name" class="form-control" required />
          </div>
          <div class="col-md-2">
            <label class="form-label small">Price (₹)</label>
            <input
              v-model.number="form.price"
              class="form-control"
              type="number"
              min="0"
              step="0.01"
            />
          </div>
          <div class="col-md-2">
            <label class="form-label small">Stock</label>
            <input
              v-model.number="form.stock"
              class="form-control"
              type="number"
              min="0"
            />
          </div>
          <div class="col-md-4">
            <label class="form-label small">Section</label>
            <select v-model="form.section_id" class="form-select">
              <option value="">— choose —</option>
              <option v-for="sec in sections" :key="sec.id" :value="sec.id">
                {{ sec.name }}
              </option>
            </select>
          </div>

          <div class="col-12">
            <label class="form-label small">Description</label>
            <input v-model="form.description" class="form-control" />
          </div>

          <div class="col-md-8">
            <label class="form-label small">Image URL</label>
            <input
              v-model="form.image"
              class="form-control"
              placeholder="https://…"
            />
          </div>

          <div class="col-md-4 d-grid">
            <button class="btn btn-primary" type="submit" :disabled="loading">
              {{
                loading
                  ? "Submitting…"
                  : form.id
                  ? "Request Update"
                  : "Request Create"
              }}
            </button>
          </div>
        </div>
        <input type="hidden" v-model="form.id" />
      </form>
    </div>

    <div v-if="loadingList" class="text-center py-4">
      <div class="spinner-border text-primary"></div>
    </div>

    <div class="row gy-3">
      <div v-for="p in products" :key="p.id" class="col-md-4">
        <div class="card h-100 shadow-sm">
          <div class="ratio ratio-4x3">
            <img
              :src="p.image || placeholder"
              class="card-img-top object-fit-cover"
              :alt="p.name"
            />
          </div>
          <div class="card-body d-flex flex-column">
            <div>
              <div class="fw-semibold">{{ p.name }}</div>
              <div class="small text-muted">
                {{ formatPrice(p.price) }} •
                {{ p.section_name || p.category || "—" }}
              </div>
            </div>
            <div class="mt-auto d-flex gap-2">
              <button
                class="btn btn-sm btn-outline-primary"
                @click="startEdit(p)"
              >
                Edit
              </button>
              <button
                class="btn btn-sm btn-outline-danger"
                @click="requestDelete(p)"
                :disabled="submittingId === p.id"
              >
                {{ submittingId === p.id ? "Requesting…" : "Request Delete" }}
              </button>
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
  name: "ProductsManagerPage",
  data() {
    return {
      products: [],
      sections: [],
      loadingList: false,
      loading: false,
      error: "",
      submittingId: null,
      placeholder: "/placeholder.svg",
      form: {
        id: null,
        name: "",
        price: null,
        stock: null,
        section_id: null,
        description: "",
        image: "",
      },
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.loadingList = true;
      try {
        const [pRes, sRes] = await Promise.all([
          api.get("/products"),
          api.get("/sections"),
        ]);
        this.products = Array.isArray(pRes)
          ? pRes
          : pRes.data || pRes.products || [];
        this.sections = Array.isArray(sRes)
          ? sRes
          : sRes.data || sRes.sections || [];
      } catch (e) {
        console.error(e);
      } finally {
        this.loadingList = false;
      }
    },
    startEdit(p) {
      this.form = {
        id: p.id,
        name: p.name,
        price: p.price,
        stock: p.stock,
        section_id: p.section_id || p.section || p.section_id,
        description: p.description || "",
        image: p.image || "",
      };
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    async submitRequest() {
      this.loading = true;
      this.error = "";
      try {
        const action = this.form.id ? "update" : "create";
        await api.post("/requests", {
          type: "product",
          action,
          data: { ...this.form },
        });
        this.form = {
          id: null,
          name: "",
          price: null,
          stock: null,
          section_id: null,
          description: "",
          image: "",
        };
        this.fetchData();
      } catch (err) {
        this.error = (err && err.message) || "Failed to submit request";
      } finally {
        this.loading = false;
      }
    },
    async requestDelete(p) {
      if (!confirm("Request deletion of this product?")) return;
      this.submittingId = p.id;
      try {
        await api.post("/requests", {
          type: "product",
          action: "delete",
          data: { id: p.id, name: p.name },
        });
        this.fetchData();
      } catch (e) {
        console.error(e);
      } finally {
        this.submittingId = null;
      }
    },
    formatPrice(v) {
      if (v == null || isNaN(Number(v))) return "-";
      return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
      }).format(Number(v));
    },
  },
};
</script>

<style scoped>
.card img {
  object-fit: cover;
  height: 160px;
}
</style>
