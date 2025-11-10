<template>
  <div class="container py-4">
    <h4 class="mb-4">Manage Sections</h4>

    <div class="card mb-3 p-3">
      <form @submit.prevent="submitRequest">
        <div class="row g-2 align-items-end">
          <div class="col-md-5">
            <label class="form-label small">Name</label>
            <input v-model="form.name" class="form-control" required />
          </div>
          <div class="col-md-5">
            <label class="form-label small">Slug / Key</label>
            <input v-model="form.slug" class="form-control" />
          </div>
          <div class="col-md-2 d-grid">
            <button class="btn btn-primary" type="submit" :disabled="loading">
              {{
                loading
                  ? "Submitting…"
                  : editing
                  ? "Request Update"
                  : "Request Create"
              }}
            </button>
          </div>
        </div>
        <input type="hidden" v-model="form.id" />
        <div v-if="error" class="text-danger small mt-2">{{ error }}</div>
      </form>
    </div>

    <div v-if="loadingList" class="text-center py-4">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-if="!loadingList && sections.length === 0" class="text-muted">
      No sections found.
    </div>

    <div class="row gy-3">
      <div v-for="s in sections" :key="s.id" class="col-md-4">
        <div class="card h-100 shadow-sm">
          <div class="card-body d-flex flex-column">
            <div class="mb-2">
              <div class="fw-semibold">{{ s.name }}</div>
              <div class="small text-muted">{{ s.slug || "—" }}</div>
            </div>
            <div class="mt-auto d-flex gap-2">
              <button
                class="btn btn-sm btn-outline-primary"
                @click="startEdit(s)"
              >
                Edit
              </button>
              <button
                class="btn btn-sm btn-outline-danger"
                @click="requestDelete(s)"
                :disabled="submittingId === s.id"
              >
                {{ submittingId === s.id ? "Requesting…" : "Request Delete" }}
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
  name: "SectionsManagerPage",
  data() {
    return {
      sections: [],
      loadingList: false,
      loading: false,
      error: "",
      editing: false,
      submittingId: null,
      form: {
        id: null,
        name: "",
        slug: "",
      },
    };
  },
  created() {
    this.fetchSections();
  },
  methods: {
    async fetchSections() {
      this.loadingList = true;
      try {
        const res = await api.get("/sections");
        this.sections = Array.isArray(res)
          ? res
          : res.data || res.sections || [];
      } catch (e) {
        console.error(e);
      } finally {
        this.loadingList = false;
      }
    },
    startEdit(section) {
      this.editing = true;
      this.form = {
        id: section.id,
        name: section.name,
        slug: section.slug || "",
      };
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    async submitRequest() {
      this.error = "";
      this.loading = true;
      try {
        const action = this.form.id ? "update" : "create";
        const payload = {
          type: "section",
          action,
          data: {
            id: this.form.id,
            name: this.form.name,
            slug: this.form.slug,
          },
        };
        await api.put(`/sections/${this.form.id}`, {
          id: this.form.id,
          name: this.form.name,
        });
        // reset
        this.form = { id: null, name: "", slug: "" };
        this.editing = false;
        this.fetchSections();
        this.$bvToast?.toast?.call?.(null); // noop safe
      } catch (err) {
        this.error = (err && err.message) || "Failed to create request";
      } finally {
        this.loading = false;
      }
    },
    async requestDelete(section) {
      if (!confirm("Request deletion of this section?")) return;
      this.submittingId = section.id;
      try {
        await api.post("/requests", {
          type: "section",
          action: "delete",
          data: { id: section.id, name: section.name },
        });
        this.fetchSections();
      } catch (e) {
        console.error(e);
      } finally {
        this.submittingId = null;
      }
    },
  },
};
</script>

<style scoped>
.card {
  border-radius: 10px;
}
</style>
