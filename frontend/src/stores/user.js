import { defineStore } from "pinia";
import api from "@/utils/api";

export const useUserStore = defineStore("user", {
  state: () => ({
    token: localStorage.getItem("access_token") || null,
    user: (() => {
      try {
        const raw = localStorage.getItem("user");
        return raw ? JSON.parse(raw) : null;
      } catch (e) {
        console.warn("Failed to parse stored user", e);
        return null;
      }
    })(),
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    role: (state) => (state.user && state.user.role ? state.user.role : null),
    isAdmin: (state) => (state.user && state.user.role) === "admin",
  },

  actions: {
    setToken(token) {
      this.token = token;
      if (token) {
        localStorage.setItem("access_token", token);
      } else {
        localStorage.removeItem("access_token");
      }
    },

    setUser(user) {
      this.user = user;
      if (user) {
        try {
          localStorage.setItem("user", JSON.stringify(user));
        } catch (e) {
          console.warn("Failed to serialize user for storage", e);
        }
      } else {
        localStorage.removeItem("user");
      }
    },

    logout() {
      this.setToken(null);
      this.setUser(null);
      // Optionally, navigate to login page from components that call logout
    },

    // Convenience: set token + user directly (e.g., after social login)
    loginWithToken(token, user = null) {
      this.setToken(token);
      if (user) this.setUser(user);
    },

    // Call an auth endpoint to login. Default endpoint is '/auth/login'.
    // Expects the server response to include a token and user info. If your
    // API returns a different shape adjust the extraction logic below.
    async loginWithCredentials(endpoint = "/auth/login", credentials = {}) {
      const res = await api.post(endpoint, credentials);

      // Try common response shapes: { access_token, user } or { token, user }
      const token =
        res &&
        (res.access_token ||
          res.token ||
          (res.data && (res.data.access_token || res.data.token)));
      const user = res && (res.user || (res.data && res.data.user) || res);

      if (!token) {
        // If the API does not return a token, throw so caller can handle it
        throw new Error("Login response did not include a token");
      }

      this.setToken(token);
      // If `user` is a primitive (like token-only response), prefer null
      this.setUser(typeof user === "object" ? user : null);
      return { token, user };
    },
  },
});
